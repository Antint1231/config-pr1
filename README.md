# Этап 1. REPL (вариант №19)

Минимальный прототип эмулятора оболочки UNIX с графическим интерфейсом.

## Что сделано
- GUI на `tkinter`; **заголовок окна содержит имя VFS** (`Эмулятор оболочки - VFS: vfs-demo`).
- Парсер на `shlex`: аргументы в кавычках (`"my dir"`, `'a b'`) остаются одним аргументом.
- Команды-заглушки `ls` и `cd` печатают своё имя и аргументы.
- Команда `exit` закрывает окно.
- Ошибки: неизвестная команда, незакрытая кавычка.

## Запуск
Нужен Python 3.8+ (tkinter входит в стандартную поставку).
```bash
python3 emulator.py
```

## Демонстрация (вводить в окне)
```
user@vfs-demo:~$ ls
command: ls
arguments: []
user@vfs-demo:~$ ls -l "my documents" 'a b'
command: ls
arguments: ['-l', 'my documents', 'a b']
user@vfs-demo:~$ cd /home/user
command: cd
arguments: ['/home/user']
user@vfs-demo:~$ cd "unclosed
error: parse error: No closing quotation
user@vfs-demo:~$ foo bar
error: foo: command not found
user@vfs-demo:~$ exit            <- окно закрывается
```

## Файлы
- `emulator.py` — точка входа, создаёт окно
- `gui.py` — окно (вывод + строка ввода, история на стрелках вверх/вниз)
- `shell.py` — парсер и команды

## Коммит
`feat: add REPL prototype with GUI, quoted-args parser and stub commands`
