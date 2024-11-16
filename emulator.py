import os
import sys
import zipfile
import shutil
from pathlib import Path
import datetime
import calendar
import argparse

try:
    import readline
except ImportError:
    import pyreadline as readline

class ShellEmulator:
    def __init__(self, user_name, root_dir, file_system_zip, script_file=None):
        self.user_name = user_name
        self.root_dir = Path(root_dir).resolve()
        self.file_system_zip = file_system_zip
        self.script_file = script_file
        self.current_dir = self.root_dir
        self.fs = None
        self._load_file_system()

    def _load_file_system(self):
        # Пример метода для работы с файловой системой через zip файл
        if zipfile.is_zipfile(self.file_system_zip):
            with zipfile.ZipFile(self.file_system_zip, 'r') as zip_ref:
                zip_ref.extractall(self.root_dir)
            self.fs = self.root_dir

    def command_cd(self, path):
        target = Path(self.current_dir, path).resolve()
        if not target.exists():
            raise FileNotFoundError(f"cd: {path}: No such directory")
        if not target.is_dir():
            raise NotADirectoryError(f"cd: {path}: Not a directory")
        self.current_dir = target

    def command_whoami(self):
        return self.user_name

    def command_exit(self, message="Bye!"):
        return message

    def command_ls(self, show_hidden=False):
        entries = os.listdir(self.current_dir)
        if not show_hidden:
            entries = [entry for entry in entries if not entry.startswith('.')]
        return entries

    def command_tree(self):
        result = []
        for root, dirs, files in os.walk(self.current_dir):
            level = root.replace(str(self.current_dir), "").count(os.sep)
            indent = " " * 4 * level
            result.append(f"{indent}{Path(root).name}/")
            sub_indent = " " * 4 * (level + 1)
            for f in files:
                result.append(f"{sub_indent}{f}")
        return "\n".join(result)

    def command_cal(self):
        # Пример команды для отображения календаря
        now = datetime.datetime.now()
        return calendar.month(now.year, now.month)

    def command_zip(self, filename):
        # Пример использования zipfile
        zip_filename = Path(self.current_dir, filename)
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for root, dirs, files in os.walk(self.current_dir):
                for file in files:
                    zipf.write(Path(root) / file, os.path.relpath(Path(root) / file, self.current_dir))
        return f"Created {filename}"

    def command_unzip(self, filename):
        # Пример распаковки архива
        zip_filename = Path(self.current_dir, filename)
        if zipfile.is_zipfile(zip_filename):
            with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
                zip_ref.extractall(self.current_dir)
            return f"Extracted {filename}"
        return "Not a valid zip file"

    def run(self):
        """Метод для запуска эмулятора в интерактивном режиме"""
        print(f"Welcome to the shell, {self.user_name}!")
        while True:
            try:
                # Вывод приглашения с текущей директорией
                command_input = input(f"{self.user_name}@{self.current_dir}> ")
                self.process_command(command_input)
            except Exception as e:
                print(f"Error: {str(e)}")

    def process_command(self, command_input):
        """Обработка команд пользователя"""
        command_parts = command_input.split()
        if not command_parts:
            return

        command = command_parts[0].lower()

        if command == "exit":
            self.command_exit()
        elif command == "cd" and len(command_parts) > 1:
            self.command_cd(command_parts[1])
        elif command == "whoami":
            print(self.command_whoami())
        elif command == "ls":
            show_hidden = False
            if len(command_parts) > 1 and command_parts[1] == "-a":
                show_hidden = True
            print("\n".join(self.command_ls(show_hidden)))
        elif command == "tree":
            print(self.command_tree())
        elif command == "cal":
            print(self.command_cal())
        else:
            print(f"Unknown command: {command}")

# Основной блок для обработки командной строки
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Shell Emulator")
    parser.add_argument("--user", type=str, required=True, help="User name for the shell prompt")
    parser.add_argument("--fs", type=str, required=True, help="Path to the virtual file system zip")
    parser.add_argument("--script", type=str, help="Path to the startup script")

    args = parser.parse_args()

    emulator = ShellEmulator(user_name=args.user, root_dir=".", file_system_zip=args.fs, script_file=args.script)
    emulator.run()
