import asyncio
import datetime

import websockets

import GamepadManager
import GamepadParser

gamepad_dict_lock = asyncio.Lock()


async def handle_client(websocket, log_file=None):
    """Handle each WebSocket client connection (websockets v15 style)."""

    client_id = str(id(websocket))  # unique per connection
    gamepad = GamepadManager.get_or_create_gamepad(client_id)

    print(f"Client connected: {client_id}")

    try:
        async for message in websocket:
            message = message.strip()
            print(f"Received message from {client_id}: {message}")

            if log_file:
                now = datetime.datetime.now()
                timestamp = now.strftime("%H:%M:%S") + f".{now.microsecond // 1000:03d}"
                with open(log_file, "a") as f:
                    f.write(
                        f"{timestamp}: Received message from {client_id}: {message}\n"
                    )

            GamepadParser.parse_gamepad(message, gamepad)

    except websockets.exceptions.ConnectionClosed as e:
        print(f"Client disconnected: {client_id} ({e})")


def start_udp_server(ip, port, logging=False):
    """
    Drop-in replacement for old UDP server.
    Works with websockets v15.
    """

    log_file = None
    if logging:
        now = datetime.datetime.now()
        date = now.strftime("%Y%m%d-%H%M%S")
        log_file = f"logs/{date}.txt"

    print(f"Starting VirtualLeverless WebSocket server on {ip}:{port}")

    async def server_loop():
        async def handler(ws):
            await handle_client(ws, log_file)

        async with websockets.serve(handler, ip, port):
            await asyncio.Future()  # run forever

    asyncio.run(server_loop())


# Keep main block for standalone testing
if __name__ == "__main__":
    start_udp_server("0.0.0.0", 8765, logging=True)
