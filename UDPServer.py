import socket
import threading

import GamepadManager
import GamepadParser

# Used to lock dictionary to ensure thread safety, currently not used.
gamepad_dict_lock = threading.Lock()


# Function for each message, used by threads
def handle_message(data, address):
    # This function will run in a separate thread to handle each message
    ip_address = address[0]
    message = data.decode("utf-8").strip()  # Get message and trim whitespace

    # Get or create the gamepad object for this IP address
    gamepad = GamepadManager.get_or_create_gamepad(ip_address)

    # Parse the message and update the corresponding gamepad
    print(f"Received message from {ip_address}: {message}")
    GamepadParser.parse_gamepad(message, gamepad)


# Function that starts the server and awaits messages
def start_udp_server(ip, port):
    try:
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind the socket to the IP address and port
        server_address = (ip, port)
        print(f"Starting VirtualLeverless Receiver on {ip}:{port}")
        sock.bind(server_address)
        print("Waiting for a message...")
        while True:
            # Receive data
            data, address = sock.recvfrom(4096)

            # Start a new thread to handle the message
            threading.Thread(target=handle_message, args=(data, address)).start()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()


# Tests the script if executed standalone, replace the values with the IP and Port you are testing
if __name__ == "__main__":
    start_udp_server("192.168.0.17", 8080)
