"""Exercise worker lifecycle without advertising or allocating real gamepads."""

import asyncio
import threading
import time
import unittest

from BluetoothManager import BluetoothManager


class FakeReceiver:
    def __init__(self, events, fail=False, block_start=False):
        self.events = events
        self.fail = fail
        self.block_start = block_start
        self.clients = {"ble:phone-one": object(), "ble:phone-two": object()}
        self.thread_id = None
        self.stopped = False

    async def start(self):
        self.thread_id = threading.get_ident()
        self.events.append(("start", self))
        if self.fail:
            raise RuntimeError("Adapter unavailable")
        if self.block_start:
            await asyncio.Future()

    async def wait(self):
        await asyncio.Future()

    async def stop(self):
        await asyncio.sleep(0.02)
        self.clients.clear()
        self.stopped = True
        self.events.append(("stop", self))


class ManagerTests(unittest.TestCase):
    def setUp(self):
        self.events = []
        self.instances = []
        self.fail_first = False
        self.block_start = False

        def factory():
            instance = FakeReceiver(self.events, self.fail_first and not self.instances, self.block_start)
            self.instances.append(instance)
            return instance

        self.manager = BluetoothManager(factory)

    def tearDown(self):
        self.manager.close(timeout=3)

    def wait_for(self, predicate, timeout=3):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if predicate():
                return
            time.sleep(0.01)
        self.fail(f"Condition not reached; status={self.manager.status}")

    def test_start_stop_and_count_are_owned_by_worker(self):
        self.manager.start()
        self.wait_for(lambda: self.manager.status.state == "Advertising")
        self.assertEqual(self.manager.status.controllers, 2)
        self.assertNotEqual(self.instances[0].thread_id, threading.get_ident())
        self.manager.stop()
        self.wait_for(lambda: self.manager.status.state == "Stopped")
        self.assertTrue(self.instances[0].stopped)
        self.assertEqual(self.manager.status.controllers, 0)

    def test_restart_cleans_up_before_creating_next_receiver(self):
        self.manager.start()
        self.wait_for(lambda: self.manager.status.state == "Advertising")
        self.manager.restart()
        self.wait_for(lambda: len(self.instances) == 2 and self.manager.status.state == "Advertising")
        self.assertEqual([name for name, _ in self.events], ["start", "stop", "start"])
        self.assertTrue(self.instances[0].stopped)

    def test_startup_failure_is_visible_and_restart_recovers(self):
        self.fail_first = True
        with self.assertLogs("BluetoothManager", level="ERROR"):
            self.manager.start()
            self.wait_for(lambda: self.manager.status.state == "Error")
        self.assertIn("Adapter unavailable", self.manager.status.error)
        self.assertTrue(self.instances[0].stopped)
        self.manager.restart()
        self.wait_for(lambda: self.manager.status.state == "Advertising")
        self.assertEqual(len(self.instances), 2)

    def test_exit_during_startup_cleans_up_without_waiting_for_start_timeout(self):
        self.block_start = True
        self.manager.start()
        self.wait_for(lambda: bool(self.events))
        self.manager.close(timeout=2)
        self.assertEqual(self.manager.status.state, "Closed")
        self.assertTrue(self.instances[0].stopped)

    def test_repeated_start_does_not_duplicate_receiver_and_closed_cannot_restart(self):
        self.manager.start()
        self.manager.start()
        self.wait_for(lambda: self.manager.status.state == "Advertising")
        self.assertEqual(len(self.instances), 1)
        self.manager.close(timeout=2)
        self.manager.start()
        self.assertEqual(self.manager.status.state, "Closed")
        self.assertEqual(len(self.instances), 1)


if __name__ == "__main__":
    unittest.main()
