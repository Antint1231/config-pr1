#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
echo "$ python3 emulator.py --headless --script scripts/no_such_file.emu"
python3 emulator.py --headless --script scripts/no_such_file.emu
echo "exit code: $?"
echo
