"""Этап 3. Виртуальная файловая система в памяти, загрузка из CSV.

Формат CSV (первая строка — заголовок):
    path,type,content
    /docs,dir,
    /docs/hello.txt,file,SGVsbG8h
path    — абсолютный путь (вложенность задаётся самим путём);
type    — dir или file;
content — содержимое файла в base64 (для папок пусто).
Недостающие родительские папки создаются автоматически.
"""
import base64
import binascii
import csv
import os
import posixpath


class VFSError(Exception):
    """Ошибка загрузки или разбора VFS."""


class Node:
    """Узел дерева: папка (children) или файл (data)."""

    def __init__(self, name, is_dir, data=b""):
        self.name = name
        self.is_dir = is_dir
        self.data = data
        self.children = {} if is_dir else None

    def size(self):
        if self.is_dir:
            return sum(child.size() for child in self.children.values())
        return len(self.data)


def normalize(cwd, path):
    """Превращает относительный путь в абсолютный (учитывает . и ..)."""
    full = posixpath.normpath(posixpath.join(cwd, path))
    return "/" + full.lstrip("/")


class VFS:
    def __init__(self, name="empty"):
        self.name = name
        self.root = Node("", True)

    def find(self, path):
        """Возвращает узел по абсолютному пути или None."""
        node = self.root
        for part in path.split("/"):
            if not part:
                continue
            if not node.is_dir or part not in node.children:
                return None
            node = node.children[part]
        return node

    def add(self, path, is_dir, data=b""):
        parts = [p for p in path.split("/") if p]
        if any(p in (".", "..") for p in parts):
            raise VFSError(f"'.' and '..' are not allowed in path '{path}'")
        if not parts:
            if is_dir:
                return
            raise VFSError("root must be a directory")
        node = self.root
        for part in parts[:-1]:  # создаём недостающие папки
            child = node.children.get(part)
            if child is None:
                child = node.children[part] = Node(part, True)
            elif not child.is_dir:
                raise VFSError(f"'{part}' is a file, not a directory")
            node = child
        name = parts[-1]
        existing = node.children.get(name)
        if existing is not None:
            if is_dir and existing.is_dir:
                return  # папка уже создана автоматически — это нормально
            raise VFSError(f"duplicate path '{path}'")
        node.children[name] = Node(name, is_dir, data)

    def tree(self):
        """Текстовое дерево всей VFS (служебная команда vfs-tree)."""
        lines = ["/"]

        def walk(node, prefix):
            items = sorted(node.children.values(), key=lambda n: n.name)
            for i, child in enumerate(items):
                last = i == len(items) - 1
                mark = "└── " if last else "├── "
                lines.append(prefix + mark + child.name + ("/" if child.is_dir else ""))
                if child.is_dir:
                    walk(child, prefix + ("    " if last else "│   "))

        walk(self.root, "")
        return "\n".join(lines)


def load_vfs(path):
    """Читает CSV и строит VFS в памяти. При проблемах бросает VFSError."""
    try:
        f = open(path, newline="", encoding="utf-8")
    except FileNotFoundError:
        raise VFSError(f"file not found: {path}")
    except OSError as e:
        raise VFSError(f"cannot open '{path}': {e.strerror}")
    with f:
        try:
            rows = list(csv.reader(f))
        except (csv.Error, UnicodeDecodeError) as e:
            raise VFSError(f"invalid format: {e}")

    header = [c.strip().lower() for c in rows[0]] if rows else []
    if header != ["path", "type", "content"]:
        raise VFSError("invalid format: header must be 'path,type,content'")

    vfs = VFS(os.path.basename(path))
    for number, row in enumerate(rows[1:], 2):
        if not row:
            continue  # пустая строка
        if len(row) != 3:
            raise VFSError(f"invalid format: line {number}: expected 3 columns")
        item_path, item_type, content = (c.strip() for c in row)
        if not item_path.startswith("/"):
            raise VFSError(f"line {number}: path must be absolute: '{item_path}'")
        try:
            if item_type == "dir":
                if content:
                    raise VFSError("directory must have empty content")
                vfs.add(item_path, True)
            elif item_type == "file":
                try:
                    data = base64.b64decode(content, validate=True)
                except (binascii.Error, ValueError):
                    raise VFSError("content is not valid base64")
                vfs.add(item_path, False, data)
            else:
                raise VFSError(f"unknown type '{item_type}' (use dir or file)")
        except VFSError as e:
            raise VFSError(f"invalid format: line {number}: {e}")
    return vfs


def copy_node(node, name):
    """Глубокая копия узла (для cp) под новым именем."""
    new = Node(name, node.is_dir, node.data)
    if node.is_dir:
        for child in node.children.values():
            new.children[child.name] = copy_node(child, child.name)
    return new
