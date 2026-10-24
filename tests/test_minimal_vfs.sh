#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
echo "$ python3 emulator.py --headless --vfs vfs/minimal.csv --script scripts/ok_small.emu"
python3 emulator.py --headless --vfs vfs/minimal.csv --script scripts/ok_small.emu
echo "exit code: $?"
echo
