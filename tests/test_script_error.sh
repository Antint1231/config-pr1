#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
echo "$ python3 emulator.py --headless --script scripts/error.emu"
python3 emulator.py --headless --script scripts/error.emu
echo "exit code: $?"
echo
