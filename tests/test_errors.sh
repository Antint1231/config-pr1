#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_ls_missing.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_ls_missing.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_ls_option.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_ls_option.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_cd_missing.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_cd_missing.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_cd_file.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_cd_file.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_cd_too_many.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_cd_too_many.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_tail_missing.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_tail_missing.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_tail_dir.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_tail_dir.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_tail_binary.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_tail_binary.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_tail_no_args.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_tail_no_args.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_tail_bad_n.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_tail_bad_n.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_tail_n_no_value.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_tail_n_no_value.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_uname_option.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_uname_option.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_uname_operand.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_uname_operand.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_du_missing.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_du_missing.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_du_option.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_du_option.emu
echo "exit code: $?"
echo
