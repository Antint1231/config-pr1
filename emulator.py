"""Точка входа эмулятора (этапы 3-5): параметры, загрузка VFS, запуск."""
import argparse
import sys

from shell import ExitShell, Shell, ShellError
from vfs import VFS, VFSError, load_vfs


def parse_args():
    p = argparse.ArgumentParser(description="Эмулятор оболочки UNIX с VFS")
    p.add_argument("--vfs", help="путь к CSV-файлу с VFS")
    p.add_argument("--script", help="путь к стартовому скрипту")
    p.add_argument("--headless", action="store_true",
                   help="консольный режим без GUI (для автотестов)")
    return p.parse_args()


def report_load_error(message, headless):
    """Сообщает об ошибке загрузки VFS."""
    print(f"error: cannot load VFS: {message}", file=sys.stderr)
    if not headless:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Ошибка загрузки VFS", message)
        root.destroy()


def run_headless(shell, banner, script):
    """Консольный режим: тот же Shell, но без окна. Возвращает код выхода."""
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    for line in banner:
        print(line)
    try:
        if script:
            shell.run_script(script, lambda text: print(text, end=""))
            return 0
        while True:
            try:
                line = input(shell.prompt())
            except EOFError:
                print()
                return 0
            try:
                out = shell.execute(line)
            except ShellError as e:
                print(f"error: {e}")
                continue
            if out:
                print(out)
    except ExitShell:
        return 0
    except ShellError as e:  # ошибка стартового скрипта
        print(f"error: {e}", file=sys.stderr)
        return 1


def main():
    args = parse_args()
    try:
        vfs = load_vfs(args.vfs) if args.vfs else VFS("empty")
    except VFSError as e:
        report_load_error(str(e), args.headless)
        return 1

    config = {
        "vfs": args.vfs or "<not set>",
        "script": args.script or "<not set>",
        "headless": args.headless,
    }
    banner = ["[debug] emulator parameters:"]
    banner += [f"[debug]   {key} = {value}" for key, value in config.items()]
    banner.append("")

    shell = Shell(config, vfs)
    if args.headless:
        return run_headless(shell, banner, args.script)

    from gui import App
    App(shell, f"Эмулятор оболочки - VFS: {vfs.name}", banner, args.script).run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
