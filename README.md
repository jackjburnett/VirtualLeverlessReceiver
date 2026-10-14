# VirtualLeverless Receiver

## Overview

VirtualLeverless Receiver is a WebSocket-based server for Windows that enables [VirtualLeverless](https://github.com/jackjburnett/VirtualLeverless) to communicate with a PC. It creates a virtual controller for each connected client using [vgamepad](https://pypi.org/project/vgamepad/) and the [ViGEmBus driver](https://vigem.org/projects/ViGEmBus/) to simulate pressing and releasing buttons and triggers of an Xbox or PlayStation controller.

---

## Requirements

- Windows 10 or later  
- **ViGEmBus driver** installed (required for virtual controllers)
  - Download ViGEmBus: [https://github.com/nefarius/ViGEmBus/releases/tag/v1.22.0](https://github.com/nefarius/ViGEmBus/releases/tag/v1.22.0)

No Python installation is required, the server is provided as a standalone `.exe`.

---

## Quick Start

1. Install ViGEmBus if not already installed. Run the installer and follow the prompts.  
2. Download `VirtualLeverlessReceiver.exe` from the [most recent release (v2.0)](https://github.com/jackjburnett/VirtualLeverlessReceiver/releases/tag/v2.0).  
3. Set up a Cloudflare Tunnel (needed if using the official VirtualLeverless):  
   - Download and install cloudflared from [https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/)  
   - Run a tunnel to forward WebSocket traffic to the server IP/port:  
     `"cloudflared tunnel --url 127.0.0.1:8080"`  
4. Run the server:  
   - Double-click the `.exe`  
   - Or run from a terminal:  
     `"cd path\to\exe"`  
     `"VirtualLeverlessReceiver.exe"`  
5. Connect VirtualLeverless to the exposed IP/port (or the Cloudflare Tunnel URL if using remote access).

---

## Simple Installation & Usage

1. Install ViGEmBus if not already installed.  
2. Download `VirtualLeverlessReceiver.exe` from the [most recent release (v2.0)](https://github.com/jackjburnett/VirtualLeverlessReceiver/releases/tag/v2.0).  
3. Run the `.exe` by double-clicking it or via a terminal:  
   `"cd path\to\exe"`  
   `"VirtualLeverlessReceiver.exe"`  

> ⚠️ **Remote Access:** To allow VirtualLeverless to connect from outside your local network, you must use a tunneling service such as Cloudflare Tunnel. Forward WebSocket traffic to the IP/port the server is listening on.

---

## Logs

All received messages are logged with timestamps and client IDs.  

Logs are stored in a `logs` folder next to the `.exe`.

---

## Advanced Installation (Python)

If you want to run the server from source:

1. Clone the repository:  
   `"git clone https://github.com/jackjburnett/VirtualLeverlessReceiver.git"`  
   `"cd VirtualLeverlessReceiver"`  

2. Create and activate a Python virtual environment:  
   `"python -m venv venv"`  
   `"venv\Scripts\activate"`  

3. Install dependencies:  
   `"pip install -r requirements.txt"`  

4. Start the server with a custom IP/port (Default: `--ip 127.0.0.1 --port 8080`):  
   `"python VirtualLeverlessReceiver.py --ip <IP_ADDRESS> --port <PORT>"`  

For remote connections, use a tunneling service like Cloudflare Tunnel to forward WebSocket traffic.

---

## Notes

### BLE prototype (Python)

Run a standalone Windows BLE peripheral using the existing Gamepad Manager and
Parser. The Wi-Fi receiver and controller mappings are unchanged.

```powershell
python -m pip install -r requirements-ble.txt
python BLE.py
```

Use a working Python 3.9–3.13 installation, ViGEmBus, and a Windows Bluetooth
adapter that supports BLE peripheral mode. The script checks the adapter and
radio before starting. Stop it with Ctrl+C to stop advertising and release inputs.

For discovery, keep `BLE.py` running until it prints `Advertising service ...`.
Use a BLE scanner such as [nRF Connect for Mobile](https://www.nordicsemi.com/Products/Development-tools/nRF-Connect-for-mobile)
on Android/iOS, or your Unity app's BLE scan. The phone's normal Bluetooth pairing
screen may not list this custom service. Allow the scanner's requested Bluetooth
permissions, scan nearby devices, and identify the advertised service UUID below.
The device name may be missing or different from the PC name. Connect inside the
BLE app; this prototype does not require pairing in the phone's settings.

If the custom service is missing and only standard services appear, disconnect
the phone, restart the receiver, and wait for `Windows advertising state: STARTED`
before reconnecting. In nRF Connect for Android, use the connected device's
three-dot menu **Refresh services** (or **Refresh device cache**, depending on
connection state/version), then discover services again. Android may retain a
service list from before the receiver was started; see
[Nordic's service cache troubleshooting](https://devzone.nordicsemi.com/f/nordic-q-a/38930/can-t-discover-custom-service-on-android-phone/150694).
Identify the scanner entry by its advertised service UUID rather than only the
PC name. If that UUID is absent from advertisements, or the service remains
missing after refreshing, capture the receiver's startup output with `--verbose`.
The local creation/advertising messages do not prove discovery on a physical phone.

In the Unity mobile app (or a BLE test app), scan for service UUID
`d749b3ea-d666-4f2f-b49d-3e43fc6db631`, connect, and write UTF-8 commands to
characteristic `d749b3ea-d666-4f2f-b49d-3e43fc6db632`. Send one complete existing
command per write, for example `A_PRESS`, `A_RELEASE`,
`LEFT_JOYSTICK_-1.0_0.0`, or `Change gamepad type to: PS`. Writes with or without
response are supported. Start testing with writes with response so errors are
visible. Each command must fit the phone's negotiated ATT write size; this
prototype does not reassemble split writes or batch commands.

To test input, write `A_PRESS` in text/UTF-8 mode with response, then write
`A_RELEASE` as a separate command. Run `python BLE.py --log-input` to log payloads,
for example `BLE received: b'A_PRESS' (7 bytes)`, after updating the controller.
Normal operation leaves per-packet logging off to reduce console I/O in the input
path. Restart `BLE.py` after updating the script. Add `--verbose` to also see each Windows `WriteRequested`
event and the decoded command. If neither appears, check that you are writing to
the input characteristic above rather than a descriptor or another service.

To investigate delay, run `python BLE.py --timings` for a short test. It reports
queueing, Windows request retrieval, and controller processing time from the
Windows write callback to the gamepad update. It does not measure the phone's
input handling, Bluetooth airtime, or the game's display latency. The first
command also creates the virtual controller; compare later commands separately.
Disable timing/debug output when measuring normal play.

For repeated input, the phone can use Write Without Response (`Command` in many
BLE scanners), which avoids waiting for an ATT response between queued writes.
The sender must respect its platform's queue/backpressure limits and preserve
press/release order. This does not set the BLE connection interval or guarantee
lower latency for a single write. Android apps can request
[high-priority connection parameters](https://developer.android.com/reference/android/bluetooth/BluetoothGatt#requestConnectionPriority(int));
on iOS, respect
[write-without-response readiness](https://developer.apple.com/documentation/corebluetooth/cbperipheral/cansendwritewithoutresponse).

Each phone's first input write creates its own Xbox controller (up to four BLE
clients). GATT session closure deletes that phone's controller through the
existing manager, which resets its inputs. A discovered/connected phone that has
not written input does not yet allocate a controller. Type switching follows the
existing WebSocket behavior. Wi-Fi can be run separately alongside this script.

The characteristic uses plain writes without pairing/authentication; this is a
local prototype. Adapter or advertising failures stop the script and clean up;
rerun it after restoring Bluetooth. Android/iPhone discovery, input writes,
disconnect events, and multiple concurrent phones still need physical testing.
See [Microsoft's Windows GATT server documentation](https://learn.microsoft.com/en-us/windows/apps/develop/devices-sensors/gatt-server)
and [PyWinRT](https://pywinrt.readthedocs.io/en/latest/) for the native API bindings.

- The `.exe` bundles Python and all dependencies, users do not need Python installed.  
- Users must have ViGEmBus installed for virtual controllers to work.  
- The project currently targets Windows x64. For x86, a separate build is required.

---

## License

This project is licensed under the GNU General Public License (GPL). See the LICENSE file for details.

---

## Contact

For any issues or questions, contact [jackjburnett](https://github.com/jackjburnett).
