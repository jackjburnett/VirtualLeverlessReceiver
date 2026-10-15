from pathlib import Path
import tempfile
import unittest

from AppSettings import ReceiverSettings, SettingsStore


class SettingsTests(unittest.TestCase):
    def test_saved_transports_and_port_survive_reload(self):
        with tempfile.TemporaryDirectory() as directory:
            store = SettingsStore(Path(directory) / "settings.json")
            self.assertEqual(store.load().wifi_port, 8000)
            settings = ReceiverSettings(wifi_enabled=False, wifi_port=9000)
            store.save(settings)
            self.assertEqual(SettingsStore(store.path).load(), settings)

    def test_invalid_ports_and_corrupt_settings_are_rejected(self):
        for port in (0, -1, 65536, True, "8000"):
            with self.subTest(port=port), self.assertRaises(ValueError):
                ReceiverSettings(wifi_port=port)
        with tempfile.TemporaryDirectory() as directory:
            store = SettingsStore(Path(directory) / "settings.json")
            store.path.write_text('{"wifi_port": 0}', encoding="utf-8")
            with self.assertLogs("AppSettings", level="ERROR"):
                self.assertEqual(store.load(), ReceiverSettings())


if __name__ == "__main__":
    unittest.main()
