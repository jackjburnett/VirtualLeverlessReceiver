# VirtualLeverless Receiver

## Overview

VirtualLeverless Receiver is a WebSocket-based server for Windows that enables [VirtualLeverless](https://github.com/jackjburnett/VirtualLeverless) to communicate with a PC. It creates a virtual controller for each connected client using [vgamepad](https://pypi.org/project/vgamepad/) and the [ViGEmBus driver](https://vigem.org/projects/ViGEmBus/) to simulate pressing and releasing buttons and triggers of an Xbox or PlayStation controller.

---

## Requirements

- Windows 10 or later  
- **ViGEmBus driver** installed (required for virtual controllers)  
  [Download ViGEmBus](https://github.com/nefarius/ViGEmBus/releases/tag/v1.22.0)  

No Python installation is required, the server is provided as a standalone `.exe`.

---
## Quick Start
1. [Install ViGEmBus](https://github.com/nefarius/ViGEmBus/releases/tag/v1.22.0) 
 (required for virtual controllers). 
Run the installer and follow the prompts.
2. **Download `VirtualLeverlessReceiver.exe`** from the [most recent release (v2.0)](https://github.com/jackjburnett/VirtualLeverlessReceiver/releases/tag/v2.0).  
3. Optional: Set up a Cloudflare Tunnel (needed if you want VirtualLeverless to connect from outside your local network):
   - Download and install cloudflared from "https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/".
   - Run a tunnel to forward WebSocket traffic to the server IP/port: ```cloudflared tunnel --url ws://127.0.0.1:8080```
4. Run the server:
   - Double-click the .exe
   - or run from a terminal: ```
         "cd path\to\exe"
         "VirtualLeverlessReceiver.exe"```
5. Connect VirtualLeverless to the exposed IP/port (or the Cloudflare Tunnel URL if using remote access).

---

## Simple Installation & Usage

1. **Install ViGEmBus** if not already installed.  
2. **Download `VirtualLeverlessReceiver.exe`** from the [most recent release (v2.0)](https://github.com/jackjburnett/VirtualLeverlessReceiver/releases/tag/v2.0).  
3. Run the `.exe` by double-clicking it or via a terminal:

```bash
cd path\to\exe
VirtualLeverlessReceiver.exe
```

> ⚠️ **Remote Access:** To allow VirtualLeverless to connect from outside your local network, you must use a tunneling service such as [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/). Set up the tunnel to forward WebSocket traffic to the IP/port the server is listening on.

---

### Logs

All received messages are logged with timestamps and client IDs.

Logs are stored in a "logs" folder next to the .exe.


## Advanced Installation (Python)

If you want to run the server from source:
1. Clone the repository:
```bash
git clone https://github.com/jackjburnett/VirtualLeverlessReceiver.git
"cd VirtualLeverlessReceiver"
```
2. Create and activate a Python virtual environment:
```
python -m venv venv"
"venv\Scripts\activate"
```
3. Install dependencies:
```
pip install -r requirements.txt"
```
4. Start the server with a custom IP/port (Default: "--ip 127.0.0.1 --port 8080"):
```
5. "python VirtualLeverlessReceiver.py --ip <IP_ADDRESS> --port <PORT>"
```

For remote connections, you need a tunneling service like Cloudflare Tunnel to forward WebSocket traffic.

## Notes
The .exe bundles Python and all dependencies — users do not need Python installed.

Users must have ViGEmBus installed for virtual controllers to work.

The project currently targets Windows x64. For x86, a separate build is required.

## License
This project is licensed under the GNU General Public License (GPL). See the [LICENSE](LICENSE) file for details.

## Contact
For any issues or questions, contact [jackjburnett](https://github.com/jackjburnett).