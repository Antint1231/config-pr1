#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
echo "$ python3 emulator.py --headless --vfs vfs/several.csv --script scripts/ok_several.emu"
python3 emulator.py --headless --vfs vfs/several.csv --script scripts/ok_several.emu
echo "exit code: $?"
echo
