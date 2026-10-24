"""Этап 1. Точка входа: запуск GUI-эмулятора."""
from gui import App
from shell import VFS_NAME, Shell


def main():
    title = f"Эмулятор оболочки - VFS: {VFS_NAME}"
    banner = ["Эмулятор оболочки UNIX (этап 1: REPL).",
              "Команды: ls, cd, exit. Аргументы в кавычках поддерживаются.", ""]
    App(Shell(), title, banner).run()


if __name__ == "__main__":
    main()
