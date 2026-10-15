"""Run the existing BLE receiver on a worker, independently of the tray UI."""

import asyncio
import logging
import queue
import sys
import threading
from dataclasses import dataclass

from BLE import BLEReceiver

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class BluetoothStatus:
    state: str = "Stopped"
    controllers: int = 0
    error: str = ""


class BluetoothManager:
    def __init__(self, receiver_factory=BLEReceiver):
        self._receiver_factory = receiver_factory
        self._lock = threading.Lock()
        self._status = BluetoothStatus()
        self._commands = queue.SimpleQueue()
        self._thread = None
        self._loop = None
        self._wake_event = None
        self._closing = False
        self._active = None

    @property
    def status(self):
        with self._lock:
            return self._status

    def _publish(self, state, controllers=0, error=""):
        status = BluetoothStatus(state, controllers, error)
        with self._lock:
            changed = status != self._status
            self._status = status
        if changed:
            logger.info("Bluetooth %s; controllers=%d%s", state, controllers,
                        f"; {error}" if error else "")

    def start(self):
        self._submit("start")

    def stop(self):
        self._submit("stop")

    def restart(self):
        self._submit("restart")

    def shutdown(self):
        self._submit("shutdown")

    def _submit(self, command):
        with self._lock:
            if self._closing:
                return
            if command == "shutdown":
                self._closing = True
            self._commands.put(command)
            if self._thread is None or not self._thread.is_alive():
                self._thread = threading.Thread(
                    target=self._thread_main, name="BluetoothReceiver", daemon=False,
                )
                self._thread.start()
            loop, event = self._loop, self._wake_event
        if loop is not None and event is not None:
            try:
                loop.call_soon_threadsafe(event.set)
            except RuntimeError:
                pass  # The worker has already finished shutting down.

    def close(self, timeout=25):
        """Wait for cleanup after the tray event loop exits; never called by a menu action."""
        self.shutdown()
        with self._lock:
            thread = self._thread
        if thread is not None:
            thread.join(timeout)
            if thread.is_alive():
                raise RuntimeError("Bluetooth cleanup has not finished; check the receiver log.")

    def _thread_main(self):
        uninitialize = None
        try:
            if sys.platform == "win32":
                from winrt.runtime import ApartmentType, init_apartment, uninit_apartment
                init_apartment(ApartmentType.MULTI_THREADED)
                uninitialize = uninit_apartment
            asyncio.run(self._run())
        except Exception as exc:
            logger.exception("Bluetooth worker failed")
            self._publish("Error", error=str(exc))
        finally:
            with self._lock:
                self._loop = self._wake_event = None
            if uninitialize is not None:
                uninitialize()

    async def _next_command(self):
        while True:
            try:
                return self._commands.get_nowait()
            except queue.Empty:
                self._wake_event.clear()
                # A submission before the event was cleared is still in the queue.
                if not self._commands.empty():
                    continue
                await self._wake_event.wait()

    async def _run(self):
        with self._lock:
            self._loop = asyncio.get_running_loop()
            self._wake_event = asyncio.Event()
        try:
            while True:
                command = await self._next_command()
                if command in ("stop", "restart", "shutdown"):
                    await self._stop_active()
                if command == "shutdown":
                    break
                if command in ("start", "restart"):
                    if self._active is not None and not self._active.done():
                        continue
                    self._publish("Starting")
                    self._active = asyncio.create_task(self._serve())
            self._publish("Closed")
        finally:
            await self._stop_active()

    async def _stop_active(self):
        if self._active is not None:
            if not self._active.done():
                self._publish("Stopping", self.status.controllers)
                self._active.cancel()
            await asyncio.gather(self._active, return_exceptions=True)
            self._active = None
        if self.status.state != "Closed":
            self._publish("Stopped")

    async def _serve(self):
        receiver = None
        waiter = None
        failure = ""
        try:
            receiver = self._receiver_factory()
            await asyncio.wait_for(receiver.start(), timeout=20)
            waiter = asyncio.create_task(receiver.wait())
            while not waiter.done():
                self._publish("Advertising", len(receiver.clients))
                await asyncio.wait({waiter}, timeout=0.25)
            await waiter
        except asyncio.CancelledError:
            pass
        except Exception as exc:
            failure = str(exc) or type(exc).__name__
            logger.exception("Bluetooth receiver failed")
        finally:
            if waiter is not None:
                waiter.cancel()
                await asyncio.gather(waiter, return_exceptions=True)
            if receiver is not None:
                try:
                    await asyncio.wait_for(receiver.stop(), timeout=10)
                except Exception as exc:
                    logger.exception("Bluetooth cleanup failed")
                    failure = str(exc) or "Bluetooth cleanup timed out"
            if failure:
                self._publish("Error", error=failure)
