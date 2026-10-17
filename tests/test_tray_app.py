"""Tray status updates, startup compatibility, and native Windows popups."""

import ctypes
from contextlib import nullcontext
import sys
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch


@unittest.skipUnless(sys.platform == "win32", "Windows tray backend")
class TrayIconUpdateTests(unittest.TestCase):
    def setUp(self):
        from AppBranding import TRAY_ICON_NAMES
        from TrayApp import TrayApplication
        self.app = object.__new__(TrayApplication)
        self.app._tray_images = {name: object() for name in TRAY_ICON_NAMES}
        self.app._icon_name = "offline"
        self.app.icon = SimpleNamespace(icon=self.app._tray_images["offline"], title="",
                                        update_menu=Mock(), notify=Mock())

    def test_slot_changes_and_disconnects_update_the_real_tray_image_selection(self):
        from VSLink import ReceiverStatus, TransportStatus
        previous = None
        for count in (0, 1, 2, 3, 4, 3, 0):
            status = ReceiverStatus(wifi=TransportStatus("Listening", count))
            self.app._update_tray(status, previous)
            expected = f"{count}-connected" if count else "online"
            self.assertIs(self.app.icon.icon, self.app._tray_images[expected])
            self.assertIn(f"Controllers: {count}/4", self.app.icon.title)
            self.assertTrue(self.app.icon.title.startswith("VSLink\n"))
            previous = status
        stopped = ReceiverStatus()
        self.app._update_tray(stopped, previous)
        self.assertIs(self.app.icon.icon, self.app._tray_images["offline"])

    def test_failure_is_visible_notified_once_and_recovers_to_connected_artwork(self):
        from VSLink import ReceiverStatus, TransportStatus
        failed = ReceiverStatus(TransportStatus("Listening", 2),
                                TransportStatus("Error", error="Adapter unavailable"))
        self.app._update_tray(failed)
        self.assertIs(self.app.icon.icon, self.app._tray_images["error"])
        self.app.icon.notify.assert_called_once_with("Adapter unavailable", "VSLink")
        self.app._update_tray(failed, failed)
        self.app.icon.notify.assert_called_once()
        recovered = ReceiverStatus(TransportStatus("Listening", 2),
                                   TransportStatus("Advertising", 1))
        self.app._update_tray(recovered, failed)
        self.assertIs(self.app.icon.icon, self.app._tray_images["3-connected"])


@unittest.skipUnless(sys.platform == "win32", "Windows startup integration")
class StartupBrandingTests(unittest.TestCase):
    def setUp(self):
        from TrayApp import WindowsStartup
        self.startup = WindowsStartup()
        self.values = {}

        def query_value(key, name):
            if name not in self.values:
                raise FileNotFoundError(name)
            return self.values[name], 1

        def delete_value(key, name):
            if name not in self.values:
                raise FileNotFoundError(name)
            del self.values[name]

        registry = SimpleNamespace(
            HKEY_CURRENT_USER=object(), REG_SZ=1, KEY_SET_VALUE=2,
            OpenKey=Mock(return_value=nullcontext("key")),
            CreateKey=Mock(return_value=nullcontext("key")),
            QueryValueEx=Mock(side_effect=query_value),
            DeleteValue=Mock(side_effect=delete_value),
            SetValueEx=Mock(side_effect=lambda key, name, reserved, kind, value:
                            self.values.__setitem__(name, value)),
        )
        self.registry_patch = patch.dict(sys.modules, {"winreg": registry})
        self.registry_patch.start()
        self.addCleanup(self.registry_patch.stop)

    def test_existing_startup_setting_is_recognized_and_replaced_when_enabled(self):
        self.values["VirtualLeverlessReceiver"] = self.startup.command
        self.assertTrue(self.startup.enabled())
        self.startup.set_enabled(True)
        self.assertEqual(self.values, {"VSLink": self.startup.command})
        self.assertTrue(self.startup.enabled())

    def test_disabling_removes_both_startup_names_without_touching_other_apps(self):
        self.values.update({"VirtualLeverlessReceiver": self.startup.command,
                            "VSLink": self.startup.command, "Other app": "other.exe"})
        self.startup.set_enabled(False)
        self.assertEqual(self.values, {"Other app": "other.exe"})
        self.assertFalse(self.startup.enabled())


@unittest.skipUnless(sys.platform == "win32", "Native Windows tray UI")
class StatusWindowTests(unittest.TestCase):
    def setUp(self):
        import tkinter as tk
        from AppSettings import ReceiverSettings
        from TrayApp import TrayApplication
        from VSLink import ReceiverStatus
        self.root = tk.Tk()
        self.root.withdraw()
        self.manager = SimpleNamespace(status=ReceiverStatus(), settings=ReceiverSettings(),
                                       shutdown=Mock())
        self.app = TrayApplication(Path("logs"), manager=self.manager)

    def tearDown(self):
        self.app.icon.stop()
        self.root.destroy()

    def open_from_tray_thread(self):
        thread = threading.Thread(target=self.app.show_status)
        thread.start()
        thread.join(timeout=1)
        self.assertFalse(thread.is_alive(), "The tray callback must not wait for the popup")
        self.app._process_ui_requests(self.root)
        self.root.update()
        return self.app._status_window

    def test_repeated_requests_reuse_window_and_ok_closes_without_stopping_receiver(self):
        from tkinter import ttk
        window = self.open_from_tray_thread()
        self.assertEqual(window.title(), "VSLink Status")
        self.assertIs(self.open_from_tray_thread(), window)
        buttons = [widget for frame in window.winfo_children()
                   for widget in frame.winfo_children() if isinstance(widget, ttk.Button)]
        buttons[0].invoke()
        self.root.update()
        self.app._process_ui_requests(self.root)
        self.assertFalse(window.winfo_exists())
        self.assertFalse(self.app._closing.is_set())
        self.manager.shutdown.assert_not_called()
        reopened = self.open_from_tray_thread()
        self.assertIsNot(reopened, window)

    def test_native_close_button_closes_window_and_status_remains_live(self):
        from VSLink import ReceiverStatus, TransportStatus
        window = self.open_from_tray_thread()
        self.manager.status = ReceiverStatus(wifi=TransportStatus("Listening", 1), wifi_port=9000)
        self.app._process_ui_requests(self.root)
        self.assertIn("port 9000", self.app._status_label.cget("text"))
        self.assertIn("Connected controllers: 1/4", self.app._status_label.cget("text"))
        # WM_CLOSE is the message Windows sends for the title-bar cross / Alt+F4.
        hwnd = int(window.tk.call("wm", "frame", window._w), 0)
        send_message = ctypes.windll.user32.SendMessageW
        send_message.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_size_t, ctypes.c_ssize_t]
        send_message.restype = ctypes.c_ssize_t
        send_message(hwnd, 0x0010, 0, 0)
        self.root.update()
        self.app._process_ui_requests(self.root)
        self.assertFalse(window.winfo_exists())
        self.assertFalse(self.app._closing.is_set())
        self.manager.shutdown.assert_not_called()


if __name__ == "__main__":
    unittest.main()
