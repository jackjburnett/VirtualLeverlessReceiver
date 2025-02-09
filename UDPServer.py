import datetime
import socket
import threading

import GamepadManager
import GamepadParser

# Used to lock dictionary to ensure thread safety, currently not used.
gamepad_dict_lock = threading.Lock()


def handle_message(data, address, log_file=None):
    """
    This function runs in a separate thread to handle each incoming message.

    Parameters:
    data (bytes): The incoming message data
    address (tuple): The client's IP address and port
    log_file (str): The log file to write to (optional)
    """

    # Get the user's IP address from the address tuple
    ip_address = address[0]

    # Decode the message data from bytes to a string and strip whitespace
    message = data.decode("utf-8").strip()

    # Get or create the gamepad object for the user's IP address
    gamepad = GamepadManager.get_or_create_gamepad(ip_address)

    # Print the received message to the console
    print(f"Received message from {ip_address}: {message}")

    # If logging is enabled, write the message to the log file
    if log_file is not None:
        file = open(log_file, "a")
        time = (
            datetime.datetime.now().strftime("%H:%M:%S")
            + f".{datetime.datetime.now().microsecond // 1000:03d}"
        )
        file.write(f"{time}: Received message from {ip_address}: {message}")
        file.close()
    # Parse the message and update the corresponding gamepad
    GamepadParser.parse_gamepad(message, gamepad)


# Function that starts the server and awaits messages
def start_udp_server(ip, port, logging=False):
    sock = None  # Initialize sock to None
    try:
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind the socket to the IP address and port
        server_address = (ip, port)
        print(f"Starting VirtualLeverless Receiver on {ip}:{port}")
        if logging:
            now = datetime.datetime.now()
            date = now.strftime("%Y%m%d-%H%M%S")
            time = now.strftime("%H:%M:%S") + f".{now.microsecond // 1000:03d}"
            log_file = f"logs/{date}.txt"
            file = open(log_file, "a")
            file.write(f"{time}: Starting VirtualLeverless Receiver on {ip}:{port}\n")
            file.close()
        else:
            log_file = None
        sock.bind(server_address)
        print("Waiting for a message...")
        while True:
            # Receive data
            data, address = sock.recvfrom(4096)

            # Start a new thread to handle the message
            threading.Thread(
                target=handle_message, args=(data, address, log_file)
            ).start()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()


# Tests the script if executed standalone, replace the values with the IP and Port you are testing
if __name__ == "__main__":
    start_udp_server("192.168.0.17", 8080, True)
