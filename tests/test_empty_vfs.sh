#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
echo "$ python3 emulator.py --headless --script scripts/ok_empty.emu"
python3 emulator.py --headless --script scripts/ok_empty.emu
echo "exit code: $?"
echo
