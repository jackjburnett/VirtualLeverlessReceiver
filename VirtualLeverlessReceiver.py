"""
VirtualLeverless Receiver Main Application

This module serves as the main entry point for the VirtualLeverless Receiver application.
It provides command-line argument parsing, IP and port validation, and initializes the
WebSocket server for virtual gamepad connections.

Dependencies:
    argparse: Python's standard library for parsing command-line arguments
    asyncio: Python's asynchronous I/O library for running the WebSocket server
    ipaddress: Standard library for IP address validation and manipulation
    WebSocketServer: Custom module containing the WebSocket server implementation

Functions:
    validate_ip(ip): Validate IP address format using ipaddress module
    validate_port(port): Validate port number range and format
    main(): Main function that parses arguments and starts the server

The application supports:
- Custom IP address and port configuration
- Optional message logging functionality
- Input validation with helpful error messages
- Graceful error handling for invalid configurations

Usage:
    python VirtualLeverlessReceiver.py --ip 127.0.0.1 --port 8080 --logging
"""

import argparse
import asyncio
import ipaddress

from WebSocketServer import start_websocket_server


# Validates IP Address using the ipaddress module
def validate_ip(ip):
    """
    Validate an IP address to ensure it is in the correct format.

    Args:
        ip (str): The IP address to validate.

    Raises:
        ValueError: If the IP address is invalid.
    """
    try:
        # This will raise an exception if the IP is invalid
        ipaddress.ip_address(ip)
    except ValueError as e:
        raise ValueError(f"Invalid IP address: {ip}") from e


# Validates port by checking it is within correct range
def validate_port(port):
    """
    Validate a port number to ensure it is within the valid range.

    Args:
        port (int): The port number to validate.

    Raises:
        ValueError: If the port number is invalid.
    """
    if not (0 <= port <= 65535):
        raise ValueError(
            f"Invalid port number: {port}. Port must be between 0 and 65535."
        )


# Runs VirtualLeverless Receiver, checking for arguments.
if __name__ == "__main__":
    # Set up argument parsing for IP and Port
    parser = argparse.ArgumentParser(
        description="VirtualLeverless Receiver (Python UDP server)"
    )
    parser.add_argument(
        "--ip",
        "--ipaddress",
        type=str,
        default="127.0.0.1",
        help="IP address to bind the server (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        "--p",
        type=int,
        default=8080,
        help="Port number to bind the server (default: 8080)",
    )

    parser.add_argument(
        "--logging",
        "--l",
        action="store_true",
        default=False,
        help="Enables logging of data to files (omitted by default)",
    )

    # Parse arguments
    args = parser.parse_args()

    # Validate arguments
    validate_ip(args.ip)
    validate_port(args.port)

    # Start the UDP server with provided IP and Port
    asyncio.run(start_websocket_server(args.ip, args.port, args.logging))
