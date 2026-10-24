#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
echo "$ python3 emulator.py --headless --script scripts/ok.emu"
python3 emulator.py --headless --script scripts/ok.emu
echo "exit code: $?"
echo
