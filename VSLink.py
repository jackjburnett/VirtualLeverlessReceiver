"""Coordinate Wi-Fi and BLE on one worker with shared controller ownership."""

import argparse
import asyncio
from dataclasses import dataclass, replace
import logging
import queue
import sys
import threading

from AppSettings import ReceiverSettings, SettingsStore
from BLE import BLEReceiver
from ControllerRouter import ControllerRouter
from WebSocketServer import WiFiReceiver

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class TransportStatus:
    state: str = "Stopped"
    controllers: int = 0
    error: str = ""


@dataclass(frozen=True)
class ReceiverStatus:
    wifi: TransportStatus = TransportStatus()
    bluetooth: TransportStatus = TransportStatus()
    wifi_port: int = 8000

    @property
    def controllers(self):
        return self.wifi.controllers + self.bluetooth.controllers


class VirtualLeverless:
    def __init__(self, settings=None, controllers=None,
                 ble_factory=BLEReceiver, wifi_factory=WiFiReceiver):
        self.controllers = controllers if controllers is not None else ControllerRouter()
        self._settings = settings if settings is not None else ReceiverSettings()
        self._status = ReceiverStatus(wifi_port=self._settings.wifi_port)
        self._factories = {"wifi": wifi_factory, "bluetooth": ble_factory}
        self._lock = threading.Lock()
        self._commands = queue.SimpleQueue()
        self._thread = self._loop = self._wake_event = None
        self._closing = False
        self._tasks = {}
        self._applied = None

    @property
    def settings(self):
        with self._lock:
            return self._settings

    @property
    def status(self):
        with self._lock:
            return self._status

    def _publish(self, transport, state, controllers=0, error=""):
        status = TransportStatus(state, controllers, error)
        with self._lock:
            previous = getattr(self._status, transport)
            self._status = replace(self._status, **{transport: status})
        if previous != status:
            logger.info("%s %s; controllers=%d%s", transport, state, controllers,
                        f"; {error}" if error else "")

    def start(self):
        self._submit("configure", self.settings)

    def configure(self, settings):
        self._submit("configure", settings)

    def restart(self):
        self._submit("restart", self.settings)

    def shutdown(self):
        self._submit("shutdown")

    def _submit(self, command, settings=None):
        with self._lock:
            if self._closing:
                return
            if settings is not None:
                self._settings = settings
            if command == "shutdown":
                self._closing = True
            self._commands.put((command, settings))
            if self._thread is None or not self._thread.is_alive():
                self._thread = threading.Thread(target=self._thread_main,
                                                name="VSLink", daemon=False)
                self._thread.start()
            loop, event = self._loop, self._wake_event
        if loop is not None and event is not None:
            try:
                loop.call_soon_threadsafe(event.set)
            except RuntimeError:
                pass

    def close(self, timeout=25):
        self.shutdown()
        if self._thread is not None:
            self._thread.join(timeout)
            if self._thread.is_alive():
                raise RuntimeError("Receiver cleanup has not finished; check the log")

    def _thread_main(self):
        try:
            asyncio.run(self._run())
        except Exception as exc:
            logger.exception("Receiver worker failed")
            self._publish("wifi", "Error", error=str(exc))
            self._publish("bluetooth", "Error", error=str(exc))
        finally:
            with self._lock:
                self._loop = self._wake_event = None

    async def _next_command(self):
        while True:
            try:
                return self._commands.get_nowait()
            except queue.Empty:
                self._wake_event.clear()
                if not self._commands.empty():
                    continue
                await self._wake_event.wait()

    async def _run(self):
        with self._lock:
            self._loop = asyncio.get_running_loop()
            self._wake_event = asyncio.Event()
        try:
            while True:
                command, settings = await self._next_command()
                if command == "shutdown":
                    break
                await self._apply(settings, restart=command == "restart")
        finally:
            await asyncio.gather(*(self._stop(name) for name in self._factories))
            self.controllers.close()
            for name in self._factories:
                self._publish(name, "Closed")

    async def _apply(self, settings, restart=False):
        previous = self._applied
        for name in self._factories:
            enabled = getattr(settings, name + "_enabled")
            was_enabled = previous is not None and getattr(previous, name + "_enabled")
            changed_port = name == "wifi" and previous is not None and previous.wifi_port != settings.wifi_port
            if not enabled or restart or changed_port:
                await self._stop(name)
            if enabled and (not was_enabled or restart or changed_port):
                self._publish(name, "Starting")
                self._tasks[name] = asyncio.create_task(self._serve(name, settings))
        self._applied = settings
        with self._lock:
            self._status = replace(self._status, wifi_port=settings.wifi_port)

    async def _stop(self, name):
        task = self._tasks.pop(name, None)
        if task is not None:
            if not task.done():
                self._publish(name, "Stopping", getattr(self.status, name).controllers)
                task.cancel()
            await asyncio.gather(task, return_exceptions=True)
        self._publish(name, "Stopped")

    async def _serve(self, name, settings):
        receiver = waiter = uninitialize = None
        failure = ""
        try:
            # A missing WinRT package or unsupported adapter must not stop Wi-Fi.
            if name == "bluetooth" and sys.platform == "win32":
                from winrt.runtime import ApartmentType, init_apartment, uninit_apartment
                init_apartment(ApartmentType.MULTI_THREADED)
                uninitialize = uninit_apartment
            arguments = {"controllers": self.controllers}
            if name == "wifi":
                arguments["port"] = settings.wifi_port
            receiver = self._factories[name](**arguments)
            await asyncio.wait_for(receiver.start(), timeout=20)
            waiter = asyncio.create_task(receiver.wait())
            while not waiter.done():
                self._publish(name, "Listening" if name == "wifi" else "Advertising", len(receiver.clients))
                await asyncio.wait({waiter}, timeout=0.25)
            await waiter
            raise RuntimeError(f"{name} stopped unexpectedly")
        except asyncio.CancelledError:
            pass
        except Exception as exc:
            failure = str(exc) or type(exc).__name__
            logger.exception("%s receiver failed", name)
        finally:
            if waiter is not None:
                waiter.cancel()
                await asyncio.gather(waiter, return_exceptions=True)
            if receiver is not None:
                try:
                    await asyncio.wait_for(receiver.stop(), timeout=10)
                except Exception as exc:
                    logger.exception("%s cleanup failed", name)
                    failure = str(exc) or "Cleanup timed out"
            if uninitialize is not None:
                uninitialize()
            if failure:
                self._publish(name, "Error", error=failure)


def main():
    arguments = argparse.ArgumentParser(description="VSLink Wi-Fi and BLE server for VirtuaStick")
    arguments.add_argument("--port", type=int, help="Wi-Fi WebSocket port (default: saved setting or 8000)")
    arguments.add_argument("--no-wifi", action="store_true")
    arguments.add_argument("--no-bluetooth", action="store_true")
    args = arguments.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    settings = SettingsStore().load()
    changes = {}
    if args.port is not None:
        changes["wifi_port"] = args.port
    if args.no_wifi:
        changes["wifi_enabled"] = False
    if args.no_bluetooth:
        changes["bluetooth_enabled"] = False
    try:
        settings = replace(settings, **changes)
    except ValueError as exc:
        arguments.error(str(exc))
    receiver = VirtualLeverless(settings)
    receiver.start()
    try:
        # A finite wait lets Windows deliver Ctrl+C to the console entry point.
        while True:
            threading.Event().wait(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        receiver.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
