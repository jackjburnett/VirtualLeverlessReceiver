"""
WebSocket Server Module

This module provides a WebSocket server for handling virtual gamepad connections.
It manages client connections, processes gamepad input messages, and supports
dynamic gamepad type switching between Xbox and PlayStation 4 controllers.

Dependencies:
    asyncio: Python's asynchronous I/O library for concurrent operations
    datetime: Standard library for date and time operations (logging timestamps)
    websockets: WebSocket server library for handling client connections
    GamepadManager: Module for managing virtual gamepad instances
    GamepadParser: Module for parsing gamepad input messages

Functions:
    handle_client(websocket, log_file): Handle individual WebSocket client connections
    start_websocket_server(ip, port, logging): Start the WebSocket server

The server supports real-time gamepad input processing with features like:
- Multiple concurrent client connections
- Dynamic gamepad type switching via messages
- Message logging with timestamps
- Graceful client disconnection handling
- Xbox 360 and PS4 controller support
"""

import asyncio
import datetime

import websockets

import GamepadManager
import GamepadParser

gamepad_dict_lock = asyncio.Lock()


async def handle_client(websocket, log_file=None):
    client_id = str(id(websocket))  # unique per connection
    # Controllers initially generated as Xbox gamepads
    gamepad = GamepadManager.get_or_create_gamepad(client_id, gamepad_type="XBOX")

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
            if message.startswith("Change gamepad type to:"):
                # Parse the gamepad type from the message
                gamepad_type = (
                    message.replace("Change gamepad type to:", "").strip().upper()
                )
                if gamepad_type in ["XBOX", "PS"]:
                    # Delete current gamepad and create new one with specified type
                    GamepadManager.delete_gamepad(client_id)
                    gamepad = GamepadManager.get_or_create_gamepad(
                        client_id, gamepad_type
                    )
                    print(
                        f"Changed gamepad type to {gamepad_type} for client {client_id}"
                    )
                else:
                    print(f"Invalid gamepad type: {gamepad_type}. Use 'XBOX' or 'PS'")
            else:
                GamepadParser.parse_gamepad(message, gamepad)

    except websockets.exceptions.ConnectionClosed as e:
        print(f"Client disconnected: {client_id} ({e})")
        GamepadManager.delete_gamepad(client_id)


async def start_websocket_server(ip, port, logging=False):
    log_file = None
    if logging:
        now = datetime.datetime.now()
        date = now.strftime("%Y%m%d-%H%M%S")
        log_file = f"logs/{date}.txt"

    print(f"Starting VirtualLeverless Receiver on {ip}:{port}")

    async with websockets.serve(lambda ws: handle_client(ws, log_file), ip, port):
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(start_websocket_server("127.0.0.1", 8080, logging=True))
