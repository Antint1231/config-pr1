"""Этап 3. Оболочка с подключённой VFS (ls и cd пока заглушки)."""
import shlex


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
    def __init__(self, config, vfs):
        self.config = config
        self.vfs = vfs
        self.commands = {
            "ls": self.cmd_ls,
            "cd": self.cmd_cd,
            "exit": self.cmd_exit,
            "conf-dump": self.cmd_conf_dump,
            "vfs-tree": self.cmd_vfs_tree,
        }

    def prompt(self):
        return f"user@{self.vfs.name}:~$ "

    def execute(self, line):
        args = parse(line)
        if not args:
            return ""
        handler = self.commands.get(args[0])
        if handler is None:
            raise ShellError(f"{args[0]}: command not found")
        return handler(args[1:])

    def run_script(self, path, write):
        """Выполняет стартовый скрипт; останавливается на первой ошибке."""
        try:
            with open(path, encoding="utf-8") as f:
                lines = f.read().splitlines()
        except OSError as e:
            raise ShellError(f"cannot read script '{path}': {e.strerror}")
        for number, line in enumerate(lines, 1):
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            write(f"{self.prompt()}{line}\n")
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
        return "\n".join(f"{key}={value}" for key, value in self.config.items())

    def cmd_vfs_tree(self, args):
        """Служебная команда: показать всё дерево VFS."""
        return self.vfs.tree()
