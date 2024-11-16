import unittest
import tempfile
from pathlib import Path
from emulator import ShellEmulator

class TestLSCommand(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.emulator = ShellEmulator("test_user", self.test_dir.name, "test_fs.zip", "script.sh")
        (Path(self.test_dir.name) / "file.txt").touch()
        (Path(self.test_dir.name) / ".hidden.txt").touch()

    def tearDown(self):
        self.test_dir.cleanup()

    def test_ls_in_empty_dir(self):
        empty_dir = Path(self.test_dir.name) / "empty"
        empty_dir.mkdir()
        self.emulator.command_cd("empty")
        self.assertEqual(self.emulator.command_ls(), [])

    def test_ls_in_non_empty_dir(self):
        files = self.emulator.command_ls()
        self.assertIn("file.txt", files)

    def test_ls_with_hidden_files(self):
        files = self.emulator.command_ls(show_hidden=True)
        self.assertIn(".hidden.txt", files)
