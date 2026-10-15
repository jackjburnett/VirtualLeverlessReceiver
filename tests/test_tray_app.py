"""Regression checks for the status popup's real Windows close controls."""

import ctypes
import sys
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock


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
