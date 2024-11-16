import unittest
import tempfile
from pathlib import Path
from emulator import ShellEmulator

class TestOtherCommands(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.emulator = ShellEmulator("test_user", self.test_dir.name, "test_fs.zip", "script.sh")

    def tearDown(self):
        self.test_dir.cleanup()

    def test_whoami(self):
        self.assertEqual(self.emulator.command_whoami(), "test_user")

def test_cal(self):
    # Тестирование календаря для текущего месяца
    result = self.emulator.command_cal()
    # Проверяем, что в календаре есть аббревиатуры дней недели
    self.assertIn("Mo", result)  # Понедельник
    self.assertIn("Tu", result)  # Вторник
    self.assertIn("We", result)  # Среда
    self.assertIn("Th", result)  # Четверг
    self.assertIn("Fr", result)  # Пятница
    self.assertIn("Sa", result)  # Суббота
    self.assertIn("Su", result)  # Воскресенье

    def test_zip(self):
        # Тестирование команды создания архива
        self.emulator.command_cd(self.test_dir.name)  # Переходим в рабочую директорию
        self.emulator.command_ls()  # Проверяем файлы в директории
        result = self.emulator.command_zip("test_archive.zip")
        self.assertTrue(Path(self.test_dir.name, "test_archive.zip").exists())
        self.assertIn("Created test_archive.zip", result)

    def test_unzip(self):
        # Тестирование команды распаковки архива
        zip_file = Path(self.test_dir.name, "test_archive.zip")
        self.emulator.command_zip("test_archive.zip")
        result = self.emulator.command_unzip("test_archive.zip")
        self.assertTrue(Path(self.test_dir.name).exists())
        self.assertIn("Extracted test_archive.zip", result)
