"""Tray state selection and real VSLink artwork loading."""

import os
from pathlib import Path
import tempfile
import unittest

from AppBranding import TRAY_ICON_NAMES, asset_path, load_tray_icons, tray_icon_name
from VSLink import ReceiverStatus, TransportStatus


class TrayArtworkTests(unittest.TestCase):
    def test_idle_and_starting_transports_are_offline(self):
        for state in ("Stopped", "Starting", "Stopping", "Closed"):
            with self.subTest(state=state):
                status = ReceiverStatus(TransportStatus(state), TransportStatus(state))
                self.assertEqual(tray_icon_name(status), "offline")

    def test_either_ready_transport_is_online_without_controllers(self):
        for status in (
            ReceiverStatus(wifi=TransportStatus("Listening")),
            ReceiverStatus(bluetooth=TransportStatus("Advertising")),
            ReceiverStatus(TransportStatus("Listening"), TransportStatus("Advertising")),
        ):
            with self.subTest(status=status):
                self.assertEqual(tray_icon_name(status), "online")

    def test_combined_wifi_and_bluetooth_counts_use_the_matching_slot_artwork(self):
        for wifi, bluetooth in ((1, 0), (0, 2), (2, 1), (1, 3)):
            with self.subTest(wifi=wifi, bluetooth=bluetooth):
                status = ReceiverStatus(TransportStatus("Listening", wifi),
                                        TransportStatus("Advertising", bluetooth))
                self.assertEqual(tray_icon_name(status), f"{wifi + bluetooth}-connected")

    def test_errors_take_priority_even_with_connected_controllers(self):
        for failure in (TransportStatus("Error"),
                        TransportStatus("Error", error="Adapter unavailable"),
                        TransportStatus("Stopping", error="Cleanup failed")):
            for status in (ReceiverStatus(TransportStatus("Listening", 2), failure),
                           ReceiverStatus(failure, TransportStatus("Advertising", 2))):
                with self.subTest(status=status):
                    self.assertEqual(tray_icon_name(status), "error")

    def test_full_icon_is_used_if_a_future_controller_count_exceeds_four(self):
        status = ReceiverStatus(wifi=TransportStatus("Listening", 5))
        self.assertEqual(tray_icon_name(status), "4-connected")

    def test_all_pngs_load_without_depending_on_the_working_directory(self):
        previous_directory = Path.cwd()
        with tempfile.TemporaryDirectory() as directory:
            try:
                os.chdir(directory)
                images = load_tray_icons()
                self.assertTrue(asset_path("favicon.ico").is_file())
            finally:
                os.chdir(previous_directory)
        try:
            self.assertEqual(set(images), set(TRAY_ICON_NAMES))
            self.assertEqual(len({image.tobytes() for image in images.values()}), 7)
            for name, image in images.items():
                with self.subTest(icon=name):
                    self.assertEqual(image.mode, "RGBA")
                    self.assertEqual(image.width, image.height)
                    self.assertGreaterEqual(image.width, 32)
        finally:
            for image in images.values():
                image.close()


if __name__ == "__main__":
    unittest.main()
