#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/ok_cwd.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/ok_cwd.emu
echo "exit code: $?"
echo
