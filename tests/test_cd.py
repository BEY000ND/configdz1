import unittest
import tempfile
from pathlib import Path
from emulator import ShellEmulator

class TestCDCommand(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.emulator = ShellEmulator("test_user", self.test_dir.name, "test_fs.zip", "script.sh")
        (Path(self.test_dir.name) / "subdir").mkdir()

    def tearDown(self):
        self.test_dir.cleanup()

    def test_cd_to_nonexistent_directory(self):
        with self.assertRaises(FileNotFoundError):
            self.emulator.command_cd("nonexistent")

    def test_cd_to_parent_directory(self):
        sub_dir = Path(self.test_dir.name, "subdir")
        self.emulator.command_cd("subdir")
        self.assertEqual(self.emulator.current_dir, sub_dir)
        self.emulator.command_cd("..")
        self.assertEqual(self.emulator.current_dir, Path(self.test_dir.name))

    def test_cd_to_subdirectory(self):
        sub_dir = Path(self.test_dir.name, "subdir")
        self.emulator.command_cd("subdir")
        self.assertEqual(self.emulator.current_dir, sub_dir)
