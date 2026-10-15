"""BLE packet and lifecycle checks without physical phones or a ViGEm driver."""

import asyncio
import unittest
from enum import IntEnum
from types import SimpleNamespace
from unittest.mock import Mock

from BLE import BLEReceiver


class SessionStatus(IntEnum):
    CLOSED = 0
    ACTIVE = 1


class WriteOption(IntEnum):
    WRITE_WITH_RESPONSE = 0
    WRITE_WITHOUT_RESPONSE = 1


class AdvertisementStatus(IntEnum):
    CREATED = 0
    STOPPED = 1
    STARTED = 2
    ABORTED = 3
    STARTED_WITHOUT_ALL_ADVERTISEMENT_DATA = 4


class Session:
    def __init__(self, identity):
        self.device_id = SimpleNamespace(id=identity)
        self.session_status = SessionStatus.ACTIVE
        self.handler = None

    def add_session_status_changed(self, handler):
        self.handler = handler
        return 1

    def remove_session_status_changed(self, token):
        self.handler = None


class Manager:
    def __init__(self):
        self.pads = {}
        self.deleted = []

    def get_or_create_gamepad(self, identity, gamepad_type="XBOX"):
        if identity not in self.pads:
            self.pads[identity] = SimpleNamespace(type=gamepad_type)
        return self.pads[identity]

    def delete_gamepad(self, identity):
        self.deleted.append(identity)
        self.pads.pop(identity, None)


class Buffer(bytearray):
    @property
    def length(self):
        return len(self)


class WriteArgs:
    def __init__(self, session, value=b"A_PRESS", offset=0, option=WriteOption.WRITE_WITH_RESPONSE):
        self.session = session
        self.deferral = Mock()
        self.request = SimpleNamespace(
            value=Buffer(value), offset=offset, option=option,
            respond=Mock(), respond_with_protocol_error=Mock(),
        )

    async def get_request_async(self):
        return self.request


class BLETests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.manager = Manager()
        self.parser = Mock()
        self.receiver = BLEReceiver(self.manager, self.parser)
        self.receiver.loop = asyncio.get_running_loop()
        self.receiver.gatt = SimpleNamespace(
            GattSessionStatus=SessionStatus, GattWriteOption=WriteOption,
            GattServiceProviderAdvertisementStatus=AdvertisementStatus,
        )
        self.session = Session("phone-one")

    async def asyncTearDown(self):
        await self.receiver.stop()

    async def test_writes_route_to_separate_gamepads_and_complete_deferrals(self):
        first = WriteArgs(self.session, b" A_PRESS ")
        second = WriteArgs(Session("phone-two"), b"LEFT_TRIGGER_0.5")
        await self.receiver._handle_write(first, first.deferral)
        await self.receiver._handle_write(second, second.deferral)
        self.assertEqual(set(self.manager.pads), {"ble:phone-one", "ble:phone-two"})
        self.parser.parse_gamepad.assert_any_call("A_PRESS", self.manager.pads["ble:phone-one"])
        self.parser.parse_gamepad.assert_any_call("LEFT_TRIGGER_0.5", self.manager.pads["ble:phone-two"])
        first.request.respond.assert_called_once()
        first.deferral.complete.assert_called_once()

    async def test_write_without_response_and_type_switch_use_existing_modules(self):
        args = WriteArgs(self.session, option=WriteOption.WRITE_WITHOUT_RESPONSE)
        await self.receiver._handle_write(args, args.deferral)
        args.request.respond.assert_not_called()
        self.receiver._receive(self.session, "Change gamepad type to: PS")
        self.assertEqual(self.manager.pads["ble:phone-one"].type, "PS")
        self.assertEqual(self.manager.deleted, ["ble:phone-one"])
        self.parser.parse_gamepad.assert_called_once()

    async def test_invalid_writes_do_not_allocate_or_change_controllers(self):
        for value, offset in ((b"A_PRESS", 1), (b"\xff", 0), (b"", 0), (b" " * 3, 0), (b"x" * 513, 0)):
            with self.subTest(value=value[:8], offset=offset):
                args = WriteArgs(self.session, value, offset)
                with self.assertLogs("BLE", level="WARNING"):
                    await self.receiver._handle_write(args, args.deferral)
                args.request.respond_with_protocol_error.assert_called_once()
                args.deferral.complete.assert_called_once()
        self.assertEqual(self.manager.pads, {})
        self.parser.parse_gamepad.assert_not_called()

    async def test_closed_sessions_rejected_and_four_client_limit_preserves_others(self):
        for number in range(4):
            self.receiver._receive(Session(str(number)), "A_PRESS")
        with self.assertRaises(RuntimeError):
            self.receiver._receive(Session("fifth"), "A_PRESS")
        closed = Session("closed")
        closed.session_status = SessionStatus.CLOSED
        with self.assertRaises(ValueError):
            self.receiver._receive(closed, "A_PRESS")
        self.assertEqual(len(self.manager.pads), 4)

    async def test_disconnect_and_shutdown_release_only_owned_gamepads(self):
        self.manager.get_or_create_gamepad("wifi:existing")
        self.receiver._receive(self.session, "A_PRESS")
        self.receiver._receive(Session("phone-two"), "A_PRESS")
        self.session.handler(self.session, SimpleNamespace(status=SessionStatus.CLOSED))
        await asyncio.sleep(0)
        self.assertNotIn("ble:phone-one", self.manager.pads)
        await self.receiver.stop()
        self.assertEqual(set(self.manager.pads), {"wifi:existing"})

    async def test_failed_controller_creation_leaves_no_session(self):
        self.manager.get_or_create_gamepad = Mock(return_value=None)
        with self.assertRaises(RuntimeError):
            self.receiver._receive(self.session, "A_PRESS")
        self.assertEqual(self.receiver.clients, {})
        self.assertIsNone(self.session.handler)

    async def test_cancelled_cleanup_still_releases_controller_inputs(self):
        self.receiver._receive(self.session, "A_PRESS")
        args = WriteArgs(self.session, b"A_RELEASE")

        async def blocked_request():
            await asyncio.Future()

        args.get_request_async = blocked_request
        self.receiver._queue_write(args, args.deferral)
        await asyncio.sleep(0)
        cleanup = asyncio.create_task(self.receiver.stop())
        await asyncio.sleep(0)
        cleanup.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await cleanup
        self.assertEqual(self.manager.pads, {})
        self.assertEqual(self.receiver.clients, {})
        args.deferral.complete.assert_called_once()

    async def test_transient_startup_abort_and_later_adapter_failure(self):
        success = SimpleNamespace(name="SUCCESS")
        self.receiver._advertisement_changed(AdvertisementStatus.ABORTED, success)
        self.assertFalse(self.receiver._started.is_set())
        self.receiver._advertisement_changed(AdvertisementStatus.STARTED, success)
        self.assertTrue(self.receiver._started.is_set())
        self.receiver._advertisement_changed(AdvertisementStatus.ABORTED, success)
        with self.assertRaises(RuntimeError):
            await self.receiver.wait()


if __name__ == "__main__":
    unittest.main()
