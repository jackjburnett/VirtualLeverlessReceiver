 # VirtualLeverless Receiver

## Overview

VirtualLeverless Receiver is a simple Python-based UDP server that enables [VirtualLeverless](https://github.com/jackjburnett/VirtualLeverless) to communicate with a Windows PC.
VirtualLeverless Receiver creates a virtual controller for each IP address that connects to it, using the [VigEm Client](https://github.com/nefarius/ViGEmClient) to simulate the pressing and releasing of buttons and triggers of an Xbox 360 Controller.

## Installation

To run the VirtualLeverless Receiver, you need [Python 3.9+](https://www.python.org/downloads/) installed on your system.

### Dependencies

Install the dependencies using `pip`:

```bash
pip install -r requirements.txt
```

## Usage

To start VirtualLeverless Receiver, use the following command:

```bash
python VirtualLeverlessReceiver.py --ip <IP_ADDRESS> --port <PORT>
```

### Arguments
- **--ip**: The IP address to bind the server to. Default is 127.0.0.1.
- **--port**: The port number to bind the server to. Default is 8080.

### Example
To start the server on IP 192.168.1.10 and port 8080, use:
```bash
python script_name.py --ip 192.168.1.10 --port 8080
```

## License
This project is licensed under the GNU General Public License (GPL). See the [LICENSE](LICENSE) file for details.

## Contact
For any issues or questions, please contact [jackjburnett](https://github.com/jackjburnett).