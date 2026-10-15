"""Wi-Fi WebSocket transport for the existing controller command format."""

import asyncio
import datetime
import logging
from pathlib import Path
from uuid import uuid4

from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed

from ControllerRouter import ControllerRouter

logger = logging.getLogger(__name__)


class WiFiReceiver:
    def __init__(self, controllers=None, host="0.0.0.0", port=8000, log_file=None):
        self.controllers = controllers if controllers is not None else ControllerRouter()
        self.host = host
        self.port = port
        self.log_file = log_file
        self.server = None
        self.clients = {}
        self._stopping = False

    async def start(self):
        self._stopping = False
        self.server = await serve(self.handle_client, self.host, self.port,
                                  compression=None, max_size=512, close_timeout=2)
        logger.info("Wi-Fi listening on ws://%s:%s", self.host, self.port)

    async def handle_client(self, websocket):
        client_id = "wifi:" + uuid4().hex
        try:
            if self._stopping:
                await websocket.close(code=1001, reason="Receiver stopping")
                return
            try:
                self.controllers.connect(client_id)
            except RuntimeError as exc:
                logger.warning("Wi-Fi connection rejected: %s", exc)
                await websocket.close(code=1013, reason=str(exc)[:100])
                return
            self.clients[client_id] = websocket
            async for message in websocket:
                if self._stopping:
                    break
                try:
                    if isinstance(message, bytes):
                        message = message.decode("utf-8")
                    self.controllers.receive(client_id, message)
                except ValueError as exc:
                    logger.warning("Wi-Fi input rejected for %s: %s", client_id, exc)
                    await websocket.close(code=1007, reason="Invalid controller command")
                    break
                if self.log_file:
                    timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
                    with open(self.log_file, "a", encoding="utf-8") as output:
                        output.write(f"{timestamp}: Received message from {client_id}: {message.strip()}\n")
                logger.debug("Wi-Fi input from %s: %s", client_id, message)
        except ConnectionClosed:
            pass
        except Exception:
            logger.exception("Wi-Fi client failed: %s", client_id)
        finally:
            self.clients.pop(client_id, None)
            self.controllers.disconnect(client_id)

    async def wait(self):
        await self.server.wait_closed()
        if not self._stopping:
            raise RuntimeError("Wi-Fi listener stopped unexpectedly")

    async def stop(self):
        self._stopping = True
        try:
            if self.server is not None:
                self.server.close()
                await self.server.wait_closed()
        finally:
            # Also release inputs if a caller cancels a slow socket shutdown.
            for client_id in list(self.clients):
                self.clients.pop(client_id, None)
                self.controllers.disconnect(client_id)
            self.server = None


async def handle_client(websocket, log_file=None):
    """Keep the original standalone handler interface available."""
    await WiFiReceiver(log_file=log_file).handle_client(websocket)


async def start_websocket_server(ip, port, logging=False):
    """Keep the existing WiFI.py entry point and optional packet log."""
    log_file = None
    if logging:
        Path("logs").mkdir(exist_ok=True)
        log_file = Path("logs") / (datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".txt")
    receiver = WiFiReceiver(host=ip, port=port, log_file=log_file)
    try:
        await receiver.start()
        await receiver.wait()
    finally:
        await receiver.stop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(start_websocket_server("0.0.0.0", 8000, logging=True))
