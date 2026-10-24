"""Этап 5. Оболочка: добавлены cp и mv (изменяют VFS только в памяти)."""
import posixpath
import shlex

from vfs import copy_node, normalize

# Поля uname: (флаг, значение) в порядке вывода
UNAME_INFO = (
    ("s", "VFS-OS"),
    ("n", "vfs-host"),
    ("r", "1.0.0"),
    ("v", "#1 Emulator"),
    ("m", "x86_64"),
    ("o", "VFS/Emulator"),
)


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


def parse_flags(cmd, args, allowed):
    """Отделяет флаги (-l, -la ...) от остальных аргументов."""
    flags, rest = set(), []
    for arg in args:
        if arg.startswith("-") and len(arg) > 1:
            for ch in arg[1:]:
                if ch not in allowed:
                    raise ShellError(f"{cmd}: invalid option -- '{ch}'")
                flags.add(ch)
        else:
            rest.append(arg)
    return flags, rest


def fmt_size(size, human):
    """Размер в байтах или в читаемом виде (K, M, G)."""
    if not human:
        return str(size)
    value = float(size)
    for unit in "BKMG":
        if value < 1024 or unit == "G":
            break
        value /= 1024
    return f"{size}B" if unit == "B" else f"{value:.1f}{unit}"


class Shell:
    def __init__(self, config, vfs):
        self.config = config
        self.vfs = vfs
        self.cwd = "/"  # текущая папка внутри VFS
        self.commands = {
            "ls": self.cmd_ls,
            "cd": self.cmd_cd,
            "tail": self.cmd_tail,
            "uname": self.cmd_uname,
            "du": self.cmd_du,
            "cp": self.cmd_cp,
            "mv": self.cmd_mv,
            "exit": self.cmd_exit,
            "conf-dump": self.cmd_conf_dump,
            "vfs-tree": self.cmd_vfs_tree,
        }

    def prompt(self):
        return f"user@{self.vfs.name}:{self.cwd}$ "

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

    def node(self, path, cmd):
        """Находит узел VFS по пути (абсолютному или относительному)."""
        abs_path = normalize(self.cwd, path)
        node = self.vfs.find(abs_path)
        if node is None:
            raise ShellError(f"{cmd}: {path}: No such file or directory")
        return abs_path, node

    # --- служебные команды ---
    def cmd_exit(self, args):
        raise ExitShell()

    def cmd_conf_dump(self, args):
        return "\n".join(f"{key}={value}" for key, value in self.config.items())

    def cmd_vfs_tree(self, args):
        return self.vfs.tree()

    # --- ls ---
    def cmd_ls(self, args):
        """ls [-l] [-a] [путь ...]"""
        flags, paths = parse_flags("ls", args, "la")
        blocks = []
        for path in paths or ["."]:
            _, node = self.node(path, "ls")
            if node.is_dir:
                items = sorted(node.children.values(), key=lambda n: n.name)
                if "a" not in flags:  # скрытые файлы (.name) только с -a
                    items = [n for n in items if not n.name.startswith(".")]
                entries = [(n.name, n) for n in items]
            else:
                entries = [(path, node)]
            text = self.format_ls(entries, "l" in flags)
            if len(paths) > 1 and node.is_dir:
                text = f"{path}:\n{text}" if text else f"{path}:"
            blocks.append(text)
        return "\n\n".join(blocks)

    @staticmethod
    def format_ls(entries, long):
        if not long:
            return "  ".join(name for name, _ in entries)
        return "\n".join(
            f"{'d' if n.is_dir else '-'}rwxr-xr-x {n.size():>8} {name}"
            for name, n in entries)

    # --- cd ---
    def cmd_cd(self, args):
        """cd [путь]  (без аргумента — в корень)"""
        if len(args) > 1:
            raise ShellError("cd: too many arguments")
        target = args[0] if args else "/"
        abs_path, node = self.node(target, "cd")
        if not node.is_dir:
            raise ShellError(f"cd: {target}: Not a directory")
        self.cwd = abs_path
        return ""

    # --- tail ---
    def cmd_tail(self, args):
        """tail [-n N] файл ...  (по умолчанию 10 строк)"""
        count, files, i = 10, [], 0
        while i < len(args):
            arg = args[i]
            if arg == "-n":
                if i + 1 >= len(args):
                    raise ShellError("tail: option requires an argument -- 'n'")
                value = args[i + 1]
                if not value.isdigit():
                    raise ShellError(f"tail: invalid number of lines: '{value}'")
                count = int(value)
                i += 2
                continue
            if arg.startswith("-") and len(arg) > 1:
                raise ShellError(f"tail: invalid option -- '{arg[1:]}'")
            files.append(arg)
            i += 1
        if not files:
            raise ShellError("tail: missing file operand")

        blocks = []
        for path in files:
            _, node = self.node(path, "tail")
            if node.is_dir:
                raise ShellError(f"tail: error reading '{path}': Is a directory")
            try:
                text = node.data.decode("utf-8")
            except UnicodeDecodeError:
                raise ShellError(f"tail: {path}: binary file")
            lines = text.splitlines()
            body = "\n".join(lines[-count:] if count else [])
            blocks.append(f"==> {path} <==\n{body}" if len(files) > 1 else body)
        return "\n".join(blocks)

    # --- uname ---
    def cmd_uname(self, args):
        """uname [-s -n -r -v -m -o | -a]"""
        flags, rest = parse_flags("uname", args, "snrvmoa")
        if rest:
            raise ShellError(f"uname: extra operand '{rest[0]}'")
        if "a" in flags:
            flags = set("snrvmo")
        if not flags:
            flags = {"s"}
        return " ".join(value for flag, value in UNAME_INFO if flag in flags)

    # --- du ---
    def cmd_du(self, args):
        """du [-s] [-h] [путь ...]"""
        flags, paths = parse_flags("du", args, "sh")
        human = "h" in flags
        lines = []
        for path in paths or ["."]:
            _, node = self.node(path, "du")
            if node.is_dir and "s" not in flags:
                self.du_walk(node, path, human, lines)
            else:
                lines.append(f"{fmt_size(node.size(), human)}\t{path}")
        return "\n".join(lines)

    def du_walk(self, node, shown, human, lines):
        """Печатает размер каждой вложенной папки, затем самой папки."""
        for child in sorted(node.children.values(), key=lambda n: n.name):
            if child.is_dir:
                self.du_walk(child, shown.rstrip("/") + "/" + child.name, human, lines)
        lines.append(f"{fmt_size(node.size(), human)}\t{shown}")

    # --- cp и mv ---
    def cmd_cp(self, args):
        """cp [-r] источник ... приёмник"""
        flags, rest = parse_flags("cp", args, "rR")
        self.transfer("cp", rest, recursive=bool(flags), move=False)
        return ""

    def cmd_mv(self, args):
        """mv источник ... приёмник"""
        _, rest = parse_flags("mv", args, "")
        self.transfer("mv", rest, recursive=True, move=True)
        return ""

    def transfer(self, cmd, args, recursive, move):
        """Общая логика cp и mv. Если приёмник — существующая папка,
        источники кладутся внутрь неё; иначе это новое имя."""
        if not args:
            raise ShellError(f"{cmd}: missing file operand")
        if len(args) < 2:
            raise ShellError(f"{cmd}: missing destination file operand after '{args[0]}'")
        *sources, dest = args

        dest_abs = normalize(self.cwd, dest)
        dest_node = self.vfs.find(dest_abs)
        into_dir = dest_node is not None and dest_node.is_dir
        if len(sources) > 1 and not into_dir:
            raise ShellError(f"{cmd}: target '{dest}' is not a directory")

        for src in sources:
            src_abs, src_node = self.node(src, cmd)
            if src_abs == "/":
                raise ShellError(f"{cmd}: cannot {cmd} the root directory")
            if src_node.is_dir and not recursive:
                raise ShellError(f"{cmd}: -r not specified; omitting directory '{src}'")

            target_abs = posixpath.join(dest_abs, src_node.name) if into_dir else dest_abs
            if target_abs == src_abs:
                raise ShellError(f"{cmd}: '{src}' and '{dest}' are the same file")
            if src_node.is_dir and target_abs.startswith(src_abs + "/"):
                raise ShellError(f"{cmd}: cannot {cmd} '{src}' into itself")

            parent_path, name = posixpath.split(target_abs)
            parent = self.vfs.find(parent_path)
            if parent is None or not parent.is_dir:
                raise ShellError(f"{cmd}: cannot create '{dest}': No such file or directory")
            old = parent.children.get(name)
            if old is not None and old.is_dir:
                raise ShellError(f"{cmd}: cannot overwrite directory '{dest}'")
            if old is not None and src_node.is_dir:
                raise ShellError(f"{cmd}: cannot overwrite non-directory '{dest}' with directory")

            if move:  # переносим сам узел: убираем из старой папки, кладём в новую
                src_parent = self.vfs.find(posixpath.dirname(src_abs))
                del src_parent.children[src_node.name]
                src_node.name = name
                parent.children[name] = src_node
            else:  # копируем: исходный узел остаётся нетронутым
                parent.children[name] = copy_node(src_node, name)

        if self.vfs.find(self.cwd) is None:  # текущую папку могли переместить
            self.cwd = "/"
