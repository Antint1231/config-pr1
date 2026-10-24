#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
echo "$ python3 emulator.py --headless --vfs vfs/no_such.csv"
python3 emulator.py --headless --vfs vfs/no_such.csv
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/bad/bad_header.csv"
python3 emulator.py --headless --vfs vfs/bad/bad_header.csv
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/bad/bad_base64.csv"
python3 emulator.py --headless --vfs vfs/bad/bad_base64.csv
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/bad/bad_type.csv"
python3 emulator.py --headless --vfs vfs/bad/bad_type.csv
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/bad/bad_columns.csv"
python3 emulator.py --headless --vfs vfs/bad/bad_columns.csv
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/bad/duplicate.csv"
python3 emulator.py --headless --vfs vfs/bad/duplicate.csv
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/bad/empty.csv"
python3 emulator.py --headless --vfs vfs/bad/empty.csv
echo "exit code: $?"
echo
