import argparse
import ipaddress

import UDPServer


# Validates IP Address using the ipaddress module
def validate_ip(ip):
    try:
        # This will raise an exception if the IP is invalid
        ipaddress.ip_address(ip)
    except ValueError as e:
        raise ValueError(f"Invalid IP address: {ip}") from e


# Validates port by checking it is within correct range
def validate_port(port):
    if not (0 <= port <= 65535):
        raise ValueError(
            f"Invalid port number: {port}. Port must be between 0 and 65535."
        )


# TODO: COMMENT
if __name__ == "__main__":
    # Set up argument parsing for IP and Port
    parser = argparse.ArgumentParser(
        description="VirtualLeverless Receiver (Python UDP server)"
    )
    parser.add_argument(
        "--ip", type=str, required=True, help="IP address to bind the server"
    )
    parser.add_argument(
        "--port", type=int, required=True, help="Port number to bind the server"
    )

    # Parse arguments
    args = parser.parse_args()

    # Validate arguments
    validate_ip(args.ip)
    validate_port(args.port)

    # Start the UDP server with provided IP and Port
    UDPServer.start_udp_server(args.ip, args.port)
