"""Этап 2. Оболочка с конфигурацией и выполнением стартового скрипта."""
import shlex

VFS_NAME = "vfs"


class ShellError(Exception):
    """Ошибка команды: сообщение показывается пользователю."""


class ExitShell(Exception):
    """Сигнал завершения работы эмулятора."""


def parse(line):
    """Разбирает строку на аргументы; текст в кавычках остаётся одним аргументом."""
    try:
        return shlex.split(line)
    except ValueError as e:
        raise ShellError(f"parse error: {e}")


class Shell:
    def __init__(self, config):
        self.config = config  # словарь параметров запуска
        self.commands = {
            "ls": self.cmd_ls,
            "cd": self.cmd_cd,
            "exit": self.cmd_exit,
            "conf-dump": self.cmd_conf_dump,
        }

    def prompt(self):
        return f"user@{VFS_NAME}:~$ "

    def execute(self, line):
        args = parse(line)
        if not args:
            return ""
        handler = self.commands.get(args[0])
        if handler is None:
            raise ShellError(f"{args[0]}: command not found")
        return handler(args[1:])

    def run_script(self, path, write):
        """Выполняет стартовый скрипт, показывая и ввод, и вывод.
        Останавливается на первой ошибке (бросает ShellError)."""
        try:
            with open(path, encoding="utf-8") as f:
                lines = f.read().splitlines()
        except OSError as e:
            raise ShellError(f"cannot read script '{path}': {e.strerror}")
        for number, line in enumerate(lines, 1):
            if not line.strip() or line.lstrip().startswith("#"):
                continue  # пустые строки и комментарии пропускаем
            write(f"{self.prompt()}{line}\n")  # имитируем ввод пользователя
            try:
                out = self.execute(line)
            except ShellError as e:
                write(f"error: {e}\n")
                raise ShellError(f"script '{path}' stopped at line {number}")
            if out:
                write(out + "\n")

    # --- команды ---
    def cmd_ls(self, args):
        return f"command: ls\narguments: {args}"

    def cmd_cd(self, args):
        return f"command: cd\narguments: {args}"

    def cmd_exit(self, args):
        raise ExitShell()

    def cmd_conf_dump(self, args):
        """Параметры эмулятора в формате ключ=значение."""
        return "\n".join(f"{key}={value}" for key, value in self.config.items())
