#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
echo "$ python3 emulator.py --headless --vfs vfs/minimal.csv --script scripts/tree.emu"
python3 emulator.py --headless --vfs vfs/minimal.csv --script scripts/tree.emu
echo "exit code: $?"
echo
