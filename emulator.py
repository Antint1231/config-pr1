"""Этап 2. Точка входа: параметры командной строки, отладочный вывод, запуск."""
import argparse
import os
import sys

from shell import ExitShell, Shell, ShellError


def parse_args():
    p = argparse.ArgumentParser(description="Эмулятор оболочки UNIX")
    p.add_argument("--vfs", help="путь к физическому расположению VFS")
    p.add_argument("--script", help="путь к стартовому скрипту")
    p.add_argument("--headless", action="store_true",
                   help="консольный режим без GUI (для автотестов)")
    return p.parse_args()


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
    config = {
        "vfs": args.vfs or "<not set>",
        "script": args.script or "<not set>",
        "headless": args.headless,
    }
    # отладочный вывод всех заданных параметров при запуске
    banner = ["[debug] emulator parameters:"]
    banner += [f"[debug]   {key} = {value}" for key, value in config.items()]
    banner.append("")

    shell = Shell(config)
    if args.headless:
        return run_headless(shell, banner, args.script)

    from gui import App  # tkinter нужен только в графическом режиме
    vfs_name = os.path.basename(args.vfs) if args.vfs else "not set"
    App(shell, f"Эмулятор оболочки - VFS: {vfs_name}", banner, args.script).run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
