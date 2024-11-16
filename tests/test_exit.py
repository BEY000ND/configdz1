import unittest
import tempfile
from emulator import ShellEmulator

class TestExitCommand(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.emulator = ShellEmulator("test_user", self.test_dir.name, "test_fs.zip", "script.sh")

    def tearDown(self):
        self.test_dir.cleanup()

    def test_exit_command(self):
        message = self.emulator.command_exit()
        self.assertEqual(message, "Bye!")

    def test_exit_message(self):
        message = self.emulator.command_exit("Goodbye!")
        self.assertEqual(message, "Goodbye!")
