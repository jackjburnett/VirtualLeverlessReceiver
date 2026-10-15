"""Combined worker checks with real Wi-Fi sockets and a simulated BLE adapter."""

import asyncio
import socket
import threading
import time
import unittest
from dataclasses import replace
from unittest.mock import Mock

from websockets.sync.client import connect

from AppSettings import ReceiverSettings
from ControllerRouter import ControllerRouter
from VSLink import VirtualLeverless
from test_ble import Manager


class FakeBLE:
    def __init__(self, controllers, fail=False, block=False):
        self.controllers = controllers
        self.fail = fail
        self.block = block
        self.clients = {}
        self.stopped = False
        self.thread_id = None

    async def start(self):
        self.thread_id = threading.get_ident()
        if self.fail:
            raise RuntimeError("Adapter unavailable")
        if self.block:
            await asyncio.Future()
        self.controllers.receive("ble:phone", "A_PRESS")
        self.clients["ble:phone"] = object()

    async def wait(self):
        await asyncio.Future()

    async def stop(self):
        for client_id in self.clients:
            self.controllers.disconnect(client_id)
        self.clients.clear()
        self.stopped = True


def free_port():
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        return listener.getsockname()[1]


class CoordinatorTests(unittest.TestCase):
    def setUp(self):
        self.instances = []
        self.fail_ble = self.block_ble = False
        self.manager = Manager()
        self.parser = Mock()
        self.router = ControllerRouter(self.manager, self.parser)
        self.port = free_port()

        def factory(**kwargs):
            receiver = FakeBLE(**kwargs, fail=self.fail_ble, block=self.block_ble)
            self.instances.append(receiver)
            return receiver

        self.receiver = VirtualLeverless(ReceiverSettings(wifi_port=self.port), self.router, ble_factory=factory)

    def tearDown(self):
        self.receiver.close(timeout=4)
        self.assertEqual(self.manager.pads, {})

    def wait_for(self, predicate):
        deadline = time.monotonic() + 4
        while time.monotonic() < deadline:
            if predicate():
                return
            time.sleep(0.01)
        self.fail(f"Condition not reached: {self.receiver.status}")

    def test_port_change_rebinds_wifi_preserves_ble_and_shares_worker(self):
        self.receiver.start()
        self.wait_for(lambda: self.receiver.status.wifi.state == "Listening" and
                      self.receiver.status.bluetooth.state == "Advertising")
        ble_pad = self.manager.pads["ble:phone"]
        with connect(f"ws://127.0.0.1:{self.port}", proxy=None) as phone:
            await_count = self.parser.parse_gamepad.call_count + 1
            phone.send("A_RELEASE")
            self.wait_for(lambda: self.parser.parse_gamepad.call_count == await_count)
            # Mock records the executing thread as part of the side effect.
            threads = []
            self.parser.parse_gamepad.side_effect = lambda *_: threads.append(threading.get_ident())
            phone.send("B_PRESS")
            self.wait_for(lambda: bool(threads))
            self.assertEqual(threads, [self.instances[0].thread_id])
            self.assertNotEqual(threads[0], threading.get_ident())
            new_port = free_port()
            self.receiver.configure(replace(self.receiver.settings, wifi_port=new_port))
            self.wait_for(lambda: self.receiver.status.wifi_port == new_port and
                          self.receiver.status.wifi.state == "Listening")
            self.assertIs(self.manager.pads["ble:phone"], ble_pad)
            self.assertEqual(len(self.instances), 1)
            with connect(f"ws://127.0.0.1:{new_port}", proxy=None):
                self.wait_for(lambda: self.receiver.status.controllers == 2)
        with socket.socket() as probe:
            self.assertNotEqual(probe.connect_ex(("127.0.0.1", self.port)), 0)

    def test_ble_failure_leaves_wifi_running_and_restart_recovers(self):
        self.fail_ble = True
        with self.assertLogs("VirtualLeverless", level="ERROR"):
            self.receiver.start()
            self.wait_for(lambda: self.receiver.status.bluetooth.state == "Error")
        self.wait_for(lambda: self.receiver.status.wifi.state == "Listening")
        with connect(f"ws://127.0.0.1:{self.port}", proxy=None) as phone:
            phone.send("A_PRESS")
            self.wait_for(lambda: self.parser.parse_gamepad.called)
        self.fail_ble = False
        self.receiver.restart()
        self.wait_for(lambda: self.receiver.status.bluetooth.state == "Advertising")
        self.assertTrue(self.instances[0].stopped)

    def test_port_in_use_does_not_stop_ble(self):
        with socket.socket() as occupied:
            occupied.bind(("0.0.0.0", self.port))
            occupied.listen()
            with self.assertLogs("VirtualLeverless", level="ERROR"):
                self.receiver.start()
                self.wait_for(lambda: self.receiver.status.wifi.state == "Error")
            self.wait_for(lambda: self.receiver.status.bluetooth.state == "Advertising")
            self.assertEqual(set(self.manager.pads), {"ble:phone"})

    def test_toggle_does_not_restart_other_transport_and_close_cancels_start(self):
        self.receiver.start()
        self.wait_for(lambda: self.receiver.status.bluetooth.state == "Advertising")
        self.receiver.configure(replace(self.receiver.settings, wifi_enabled=False))
        self.wait_for(lambda: self.receiver.status.wifi.state == "Stopped")
        self.assertEqual(len(self.instances), 1)
        self.receiver.configure(replace(self.receiver.settings, bluetooth_enabled=False))
        self.wait_for(lambda: self.instances[0].stopped)
        self.block_ble = True
        self.receiver.configure(replace(self.receiver.settings, bluetooth_enabled=True))
        self.wait_for(lambda: len(self.instances) == 2 and self.instances[1].thread_id is not None)
        self.receiver.close(timeout=2)
        self.assertEqual(self.receiver.status.bluetooth.state, "Closed")
        self.assertTrue(self.instances[1].stopped)


if __name__ == "__main__":
    unittest.main()
