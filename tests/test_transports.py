"""Exercise real WebSockets alongside BLE routing without physical controllers."""

import asyncio
from types import SimpleNamespace
import unittest
from unittest.mock import Mock

from websockets.asyncio.client import connect

from BLE import BLEReceiver
from ControllerRouter import ControllerRouter
from WebSocketServer import WiFiReceiver
from test_ble import Manager, Session, SessionStatus


class TransportTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.manager = Manager()
        self.parser = Mock()
        self.controllers = ControllerRouter(self.manager, self.parser)
        self.ble = BLEReceiver(controllers=self.controllers)
        self.ble.loop = asyncio.get_running_loop()
        self.ble.gatt = SimpleNamespace(GattSessionStatus=SessionStatus)
        self.wifi = WiFiReceiver(self.controllers, host="127.0.0.1", port=0)
        await self.wifi.start()
        port = self.wifi.server.sockets[0].getsockname()[1]
        self.url = f"ws://127.0.0.1:{port}"

    async def asyncTearDown(self):
        await self.wifi.stop()
        await self.ble.stop()
        self.assertEqual(self.manager.pads, {})

    async def wait_for(self, predicate):
        async with asyncio.timeout(3):
            while not predicate():
                await asyncio.sleep(0.01)

    async def test_both_transports_use_same_parser_and_normal_close_releases_only_wifi(self):
        self.ble._receive(Session("phone"), "A_PRESS")
        ble_pad = self.manager.pads["ble:phone"]
        async with connect(self.url, proxy=None) as phone:
            await phone.send("A_PRESS")
            await self.wait_for(lambda: self.parser.parse_gamepad.call_count == 2)
            wifi_id = next(iter(self.wifi.clients))
            wifi_pad = self.manager.pads[wifi_id]
            self.assertTrue(wifi_id.startswith("wifi:"))
            self.assertIsNot(ble_pad, wifi_pad)
            self.parser.parse_gamepad.assert_any_call("A_PRESS", ble_pad)
            self.parser.parse_gamepad.assert_any_call("A_PRESS", wifi_pad)
            await phone.send("Change gamepad type to: PS")
            await self.wait_for(lambda: self.manager.pads[wifi_id].type == "PS")
            await phone.send("CROSS_PRESS")
            await self.wait_for(lambda: self.parser.parse_gamepad.call_count == 3)
            self.parser.parse_gamepad.assert_called_with("CROSS_PRESS", self.manager.pads[wifi_id])
        await self.wait_for(lambda: not self.wifi.clients)
        self.assertEqual(set(self.manager.pads), {"ble:phone"})

    async def test_four_slot_limit_is_shared_and_a_disconnect_frees_a_slot(self):
        for number in range(3):
            self.ble._receive(Session(str(number)), "A_PRESS")
        async with connect(self.url, proxy=None):
            async with connect(self.url, proxy=None) as fifth:
                await fifth.wait_closed()
                self.assertEqual(fifth.close_code, 1013)
            self.assertEqual(len(self.manager.pads), 4)
        await self.wait_for(lambda: not self.wifi.clients)
        async with connect(self.url, proxy=None) as replacement:
            await replacement.send("B_PRESS")
            await self.wait_for(lambda: len(self.manager.pads) == 4)

    async def test_invalid_utf8_and_abrupt_network_loss_release_inputs(self):
        self.ble._receive(Session("phone"), "A_PRESS")
        async with connect(self.url, proxy=None) as phone:
            await phone.send(b"\xff")
            await phone.wait_closed()
            self.assertEqual(phone.close_code, 1007)
        await self.wait_for(lambda: not self.wifi.clients)
        phone = await connect(self.url, proxy=None)
        await phone.send("A_PRESS")
        await self.wait_for(lambda: bool(self.wifi.clients))
        phone.transport.abort()
        await phone.wait_closed()
        await self.wait_for(lambda: not self.wifi.clients)
        self.assertEqual(set(self.manager.pads), {"ble:phone"})

    async def test_stopping_wifi_preserves_ble_and_invalid_ble_type_does_not_allocate(self):
        self.ble._receive(Session("phone"), "A_PRESS")
        async with connect(self.url, proxy=None) as phone:
            await phone.send("A_PRESS")
            await self.wait_for(lambda: bool(self.wifi.clients))
            await self.wifi.stop()
            await phone.wait_closed()
        self.assertEqual(set(self.manager.pads), {"ble:phone"})
        with self.assertRaises(ValueError):
            self.ble._receive(Session("invalid"), "Change gamepad type to: INVALID")
        self.assertEqual(set(self.manager.pads), {"ble:phone"})


if __name__ == "__main__":
    unittest.main()
