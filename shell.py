"""Этап 1. Парсер команд и команды-заглушки."""
import shlex

VFS_NAME = "vfs-demo"


class ShellError(Exception):
    """Ошибка команды: сообщение показывается пользователю."""


class ExitShell(Exception):
    """Сигнал завершения работы эмулятора."""


def parse(line):
    """Разбирает строку на аргументы; текст в кавычках остаётся одним аргументом."""
    try:
        return shlex.split(line)
    except ValueError as e:  # например, незакрытая кавычка
        raise ShellError(f"parse error: {e}")


class Shell:
    def __init__(self):
        self.commands = {
            "ls": self.cmd_ls,
            "cd": self.cmd_cd,
            "exit": self.cmd_exit,
        }

    def prompt(self):
        return f"user@{VFS_NAME}:~$ "

    def execute(self, line):
        """Выполняет строку и возвращает текст вывода."""
        args = parse(line)
        if not args:
            return ""
        handler = self.commands.get(args[0])
        if handler is None:
            raise ShellError(f"{args[0]}: command not found")
        return handler(args[1:])

    # --- команды-заглушки: печатают своё имя и аргументы ---
    def cmd_ls(self, args):
        return f"command: ls\narguments: {args}"

    def cmd_cd(self, args):
        return f"command: cd\narguments: {args}"

    def cmd_exit(self, args):
        raise ExitShell()
