# Build the Wi-Fi/BLE tray executable without machine-specific DLL paths.
from PyInstaller.utils.hooks import collect_dynamic_libs, collect_submodules

a = Analysis(
    ["Receiver.pyw"],
    binaries=collect_dynamic_libs("vgamepad") + collect_dynamic_libs("winrt"),
    datas=[("LICENSE", ".")],
    hiddenimports=["pystray._win32"] + collect_submodules("winrt"),
    excludes=["PySide6", "PyQt5"],
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, a.binaries, a.datas, [],
    name="VirtualLeverlessReceiver",
    icon="assets/receiver.ico",
    console=False,
    debug=False,
    strip=False,
    upx=False,
)
