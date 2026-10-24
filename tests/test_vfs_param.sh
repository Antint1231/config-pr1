#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
echo "$ python3 emulator.py --headless --vfs data/my_vfs.csv --script scripts/ok.emu"
python3 emulator.py --headless --vfs data/my_vfs.csv --script scripts/ok.emu
echo "exit code: $?"
echo
