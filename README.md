# Этап 2. Конфигурация

К прототипу этапа 1 добавлены параметры командной строки и стартовый скрипт.

## Что сделано
- Параметры: `--vfs ПУТЬ` (расположение VFS), `--script ПУТЬ` (стартовый скрипт).
  Дополнительно `--headless` — консольный режим для автотестов.
- При запуске выводится отладочная печать всех параметров (`[debug] ...`).
- Стартовый скрипт: показывает и ввод (`user@vfs:~$ команда`), и вывод; пустые строки и `#`-комментарии пропускаются;
  **останавливается на первой ошибке** и сообщает номер строки.
- Служебная команда `conf-dump` печатает параметры в виде `ключ=значение`.
- Тесты — скрипты реальной ОС (`tests/*.sh` и `tests/*.bat`).

## Запуск
```bash
python3 emulator.py --vfs data/my_vfs.csv --script scripts/ok.emu
```

## Пример (стартовый скрипт с ошибкой)
```
[debug] emulator parameters:
[debug]   vfs = <not set>
[debug]   script = scripts/error.emu
[debug]   headless = False

user@vfs:~$ ls
command: ls
arguments: []
user@vfs:~$ unknown-cmd arg
error: unknown-cmd: command not found
error: script 'scripts/error.emu' stopped at line 3
```

## Тесты (скрипты реальной ОС)

В папке `tests/` лежат пары `test_*.sh` (Linux/macOS/Git Bash) и `test_*.bat` (Windows).
Они запускают эмулятор в консольном режиме `--headless`, поэтому выполняются без окна.

```bash
sh tests/run_all.sh        # Linux / macOS / Git Bash
tests\run_all.bat          # Windows
```

Чтобы увидеть то же самое **в окне GUI**, запустите вручную без `--headless`, например:
`python3 emulator.py --vfs data/my_vfs.csv --script scripts/ok.emu`

## Коммит
`feat: add command-line parameters, startup script and conf-dump`
