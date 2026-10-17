"""VSLink branding and tray artwork shared by the source and bundled app."""

from pathlib import Path

from PIL import Image

APP_NAME = "VSLink"
TRAY_ICON_NAMES = ("error", "offline", "online", "1-connected", "2-connected",
                   "3-connected", "4-connected")


def asset_path(filename):
    # PyInstaller preserves this module's location relative to bundled data.
    return Path(__file__).resolve().parent / "assets" / filename


def tray_icon_name(status):
    """Prefer errors, then the combined controller count, then availability."""
    transports = (status.wifi, status.bluetooth)
    if any(transport.error or transport.state == "Error" for transport in transports):
        return "error"
    if status.controllers > 0:
        return f"{min(status.controllers, 4)}-connected"
    if status.wifi.state == "Listening" or status.bluetooth.state == "Advertising":
        return "online"
    return "offline"


def load_tray_icons():
    """Load each PNG once and release its file handle before the tray starts."""
    images = {}
    for name in TRAY_ICON_NAMES:
        with Image.open(asset_path(name + ".png")) as image:
            images[name] = image.convert("RGBA")
    return images
