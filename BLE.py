"""Standalone Windows BLE controller receiver using the existing gamepad modules.

Phones act as BLE centrals and write one existing UTF-8 controller command per
GATT write. A controller is allocated on the first write, not merely discovery.
"""

import argparse
import asyncio
import logging
import sys
from time import perf_counter
from uuid import UUID

SERVICE_UUID = UUID("d749b3ea-d666-4f2f-b49d-3e43fc6db631")
INPUT_UUID = UUID("d749b3ea-d666-4f2f-b49d-3e43fc6db632")
logger = logging.getLogger(__name__)


class BLEReceiver:
    def __init__(self, manager=None, parser=None, log_input=False, timings=False):
        self.manager = manager
        self.parser = parser
        self.log_input = log_input
        self.timings = timings
        self.provider = None
        self.characteristic = None
        self.clients = {}  # ble:<Windows device ID> -> (GattSession, event token)
        self._write_token = None
        self._advertisement_token = None
        self._pending = set()
        self._write_lock = asyncio.Lock()
        self._started = asyncio.Event()
        self._finished = asyncio.Event()
        self._stopping = False
        self._failure = None

    async def start(self):
        if sys.platform != "win32":
            raise RuntimeError("This BLE receiver requires Windows.")
        # Import projections only when starting; --help does not need WinRT/ViGEm.
        import winrt.windows.foundation  # noqa: F401
        import winrt.windows.foundation.collections  # noqa: F401
        import winrt.windows.devices.enumeration  # noqa: F401
        import winrt.windows.storage.streams  # noqa: F401
        from winrt.windows.devices.bluetooth import BluetoothAdapter, BluetoothError
        from winrt.windows.devices.radios import RadioState
        from winrt.windows.devices.bluetooth import genericattributeprofile as gatt

        self.gatt = gatt
        self.loop = asyncio.get_running_loop()
        adapter = await BluetoothAdapter.get_default_async()
        if adapter is None or not adapter.is_peripheral_role_supported:
            raise RuntimeError("No Bluetooth adapter with BLE peripheral support found.")
        radio = await adapter.get_radio_async()
        if radio is None or radio.state != RadioState.ON:
            raise RuntimeError("Turn on the Windows Bluetooth radio first.")
        if self.manager is None:
            import GamepadManager
            self.manager = GamepadManager
        if self.parser is None:
            import GamepadParser
            self.parser = GamepadParser

        result = await gatt.GattServiceProvider.create_async(SERVICE_UUID)
        if result.error != BluetoothError.SUCCESS:
            raise RuntimeError(f"GATT service creation failed: {result.error.name}")
        self.provider = result.service_provider
        logger.info("Windows created local GATT service: %s", self.provider.service.uuid)
        parameters = gatt.GattLocalCharacteristicParameters()
        parameters.characteristic_properties = (
            gatt.GattCharacteristicProperties.WRITE
            | gatt.GattCharacteristicProperties.WRITE_WITHOUT_RESPONSE
        )
        parameters.write_protection_level = gatt.GattProtectionLevel.PLAIN
        parameters.user_description = "VirtualLeverless controller input"
        result = await self.provider.service.create_characteristic_async(INPUT_UUID, parameters)
        if result.error != BluetoothError.SUCCESS:
            raise RuntimeError(f"Input characteristic creation failed: {result.error.name}")
        self.characteristic = result.characteristic
        logger.info("Windows created input characteristic: %s", self.characteristic.uuid)
        self._write_token = self.characteristic.add_write_requested(self._on_write)
        self._advertisement_token = self.provider.add_advertisement_status_changed(self._on_advertisement)
        advertising = gatt.GattServiceProviderAdvertisingParameters()
        advertising.is_connectable = True
        advertising.is_discoverable = True
        self.provider.start_advertising_with_parameters(advertising)
        try:
            await asyncio.wait_for(self._started.wait(), timeout=10)
        except asyncio.TimeoutError as exc:
            raise RuntimeError("BLE advertising did not start; check the adapter and Windows Bluetooth permissions.") from exc
        if self._failure:
            raise self._failure
        logger.info("Windows advertising state: %s", self.provider.advertisement_status.name)
        logger.info("Advertising service %s; input characteristic %s", SERVICE_UUID, INPUT_UUID)
        logger.info("Discover this service using a BLE scanner or your mobile app; use the service UUID above.")
        logger.info("If only standard services appear, refresh the phone's service cache and reconnect after advertising starts.")

    def _on_advertisement(self, sender, args):
        try:
            self.loop.call_soon_threadsafe(self._advertisement_changed, args.status, args.error)
        except Exception:
            logger.exception("Unable to handle Bluetooth advertising event")

    def _advertisement_changed(self, status, error):
        logger.debug("Bluetooth advertising status: %s (%s)", status.name, error.name)
        statuses = self.gatt.GattServiceProviderAdvertisementStatus
        if status == statuses.STARTED:
            self._started.set()
        elif status == statuses.STARTED_WITHOUT_ALL_ADVERTISEMENT_DATA:
            logger.warning("Windows could not include all advertisement data; verify service discovery on phones.")
            self._started.set()
        elif (not self._stopping and self._started.is_set()
              and status in (statuses.ABORTED, statuses.STOPPED)):
            # Some Windows adapters emit ABORTED/SUCCESS before STARTED during
            # initialization. Startup waits for STARTED or its timeout above.
            self._failure = RuntimeError(f"Bluetooth advertising stopped: {status.name}, {error.name}")
            self._started.set()
            self._finished.set()

    def _on_write(self, sender, args):
        # Windows calls this on its own thread. Defer the response and perform all
        # gamepad operations on our asyncio loop, including disconnect cleanup.
        deferral = None
        try:
            received_at = perf_counter()
            logger.debug("BLE WriteRequested event received")
            deferral = args.get_deferral()
            self.loop.call_soon_threadsafe(self._queue_write, args, deferral, received_at)
        except Exception:
            if deferral is not None:
                deferral.complete()
            logger.exception("Unable to schedule BLE input")

    def _queue_write(self, args, deferral, received_at=None):
        if self._stopping:
            deferral.complete()
            return
        task = asyncio.create_task(self._handle_write(args, deferral, received_at))
        self._pending.add(task)
        task.add_done_callback(self._pending.discard)

    def _respond(self, request, error=None):
        if request.option == self.gatt.GattWriteOption.WRITE_WITH_RESPONSE:
            if error is None:
                request.respond()
            else:
                request.respond_with_protocol_error(error)

    async def _handle_write(self, args, deferral, received_at=None):
        request = None
        if received_at is None:
            received_at = perf_counter()
        try:
            async with self._write_lock:
                request_started = perf_counter()
                request = await asyncio.wait_for(args.get_request_async(), timeout=5)
                request_ready = perf_counter()
                if request is None:
                    logger.warning("BLE write canceled before its data became available")
                    return  # Windows canceled the request.
                if self._stopping:
                    logger.warning("BLE write rejected: receiver is stopping")
                    self._respond(request, 0x80)
                    return
                data = bytes(memoryview(request.value)[:request.value.length])
                if request.offset != 0:
                    logger.warning("BLE write rejected: offset %d; send one complete command per write", request.offset)
                    self._respond(request, 0x07)  # ATT invalid offset; no fragmentation.
                    return
                if not data or len(data) > 512:
                    logger.warning("BLE write rejected: invalid payload length %d", len(data))
                    self._respond(request, 0x0D)  # ATT invalid attribute value length.
                    return
                self._receive(args.session, data.decode("utf-8").strip())
                applied_at = perf_counter()
                self._respond(request)
                # Console output follows the controller update. Keep normal input
                # quiet so terminal I/O does not delay the next queued command.
                if self.log_input or logger.isEnabledFor(logging.DEBUG):
                    logger.info("BLE received: %r (%d bytes)", data, len(data))
                    logger.debug("BLE write option: %s; offset: %d", request.option.name, request.offset)
                if self.timings:
                    logger.info(
                        "BLE PC processing: %.2f ms (queue %.2f, request %.2f, controller %.2f); excludes phone/radio delay",
                        (applied_at - received_at) * 1000,
                        (request_started - received_at) * 1000,
                        (request_ready - request_started) * 1000,
                        (applied_at - request_ready) * 1000,
                    )
        except Exception:
            logger.exception("BLE input rejected")
            if request is not None:
                try:
                    self._respond(request, 0x80)  # Application error.
                except Exception:
                    logger.exception("Unable to respond to BLE write")
        finally:
            try:
                deferral.complete()
            except Exception:
                logger.exception("Unable to complete BLE write deferral")

    def _receive(self, session, message):
        if not message:
            raise ValueError("Empty controller command")
        if session.session_status == self.gatt.GattSessionStatus.CLOSED:
            raise ValueError("BLE session is closed")
        client_id = "ble:" + session.device_id.id
        logger.debug("Controller command from %s: %r", client_id, message)
        gamepad_type = None
        if message.startswith("Change gamepad type to:"):
            gamepad_type = message.replace("Change gamepad type to:", "").strip().upper()
            if gamepad_type not in ("XBOX", "PS"):
                raise ValueError("Invalid gamepad type; use XBOX or PS")
        if client_id not in self.clients:
            if len(self.clients) >= 4:
                raise RuntimeError("All four BLE controllers are in use")
            gamepad = self.manager.get_or_create_gamepad(client_id, "XBOX")
            if gamepad is None:
                raise RuntimeError("Unable to create virtual controller; check ViGEmBus")
            try:
                token = session.add_session_status_changed(
                    lambda sender, args: self._on_session(client_id, session, args)
                )
            except Exception:
                self.manager.delete_gamepad(client_id)
                raise
            self.clients[client_id] = (session, token)
            logger.info("BLE controller connected (%d/4): %s", len(self.clients), client_id)
        if gamepad_type:
            self.manager.delete_gamepad(client_id)
            gamepad = self.manager.get_or_create_gamepad(client_id, gamepad_type)
        else:
            gamepad = self.manager.get_or_create_gamepad(client_id)
        if gamepad is None:
            self._disconnect(client_id)
            raise RuntimeError("Unable to create virtual controller; check ViGEmBus")
        if not gamepad_type:
            self.parser.parse_gamepad(message, gamepad)

    def _on_session(self, client_id, session, args):
        try:
            if args.status == self.gatt.GattSessionStatus.CLOSED:
                self.loop.call_soon_threadsafe(self._session_closed, client_id, session)
        except Exception:
            logger.exception("Unable to handle BLE disconnect")

    def _session_closed(self, client_id, session):
        if client_id in self.clients and self.clients[client_id][0] is session:
            self._disconnect(client_id)

    def _disconnect(self, client_id):
        client = self.clients.pop(client_id, None)
        if client is None:
            return
        session, token = client
        try:
            session.remove_session_status_changed(token)
        except Exception:
            logger.exception("Unable to remove BLE session handler")
        try:
            self.manager.delete_gamepad(client_id)  # Existing reset/update cleanup.
        except Exception:
            logger.exception("Unable to release BLE controller %s", client_id)
        logger.info("BLE controller disconnected: %s", client_id)

    async def wait(self):
        await self._finished.wait()
        if self._failure:
            raise self._failure

    async def stop(self):
        self._stopping = True
        for remove, token in (
            (self.characteristic.remove_write_requested if self.characteristic else None, self._write_token),
            (self.provider.remove_advertisement_status_changed if self.provider else None, self._advertisement_token),
        ):
            if remove is not None and token is not None:
                try:
                    remove(token)
                except Exception:
                    logger.exception("Unable to remove Bluetooth handler")
        if self.provider is not None:
            try:
                self.provider.stop_advertising()
            except Exception:
                logger.exception("Unable to stop Bluetooth advertising")
        # Drain acquired deferrals before releasing sessions and gamepads.
        if self._pending:
            await asyncio.gather(*self._pending, return_exceptions=True)
        for client_id in list(self.clients):
            self._disconnect(client_id)
        self.characteristic = self.provider = None
        self._write_token = self._advertisement_token = None
        self._finished.set()


async def run(log_input=False, timings=False):
    receiver = BLEReceiver(log_input=log_input, timings=timings)
    try:
        await receiver.start()
        await receiver.wait()
    finally:
        await receiver.stop()


def main():
    arguments = argparse.ArgumentParser(description="Windows BLE controller receiver")
    arguments.add_argument("--verbose", action="store_true", help="Enable debug logging")
    arguments.add_argument("--log-input", action="store_true", help="Log received packets after updating the gamepad")
    arguments.add_argument("--timings", action="store_true", help="Log PC processing time; excludes phone/radio delay")
    args = arguments.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    try:
        asyncio.run(run(log_input=args.log_input, timings=args.timings))
    except KeyboardInterrupt:
        logger.info("BLE receiver stopped")
    except ImportError as exc:
        logger.error("Missing dependency; install requirements-ble.txt: %s", exc)
        return 1
    except Exception as exc:
        logger.error("Cannot run BLE receiver: %s", exc)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
