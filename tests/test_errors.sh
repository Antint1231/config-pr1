#!/bin/sh
cd "$(dirname "$0")/.." || exit 1
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_cp_dir_no_r.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_cp_dir_no_r.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_cp_missing.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_cp_missing.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_cp_no_args.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_cp_no_args.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_cp_no_dest.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_cp_no_dest.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_cp_same.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_cp_same.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_cp_into_self.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_cp_into_self.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_cp_no_parent.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_cp_no_parent.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_cp_over_dir.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_cp_over_dir.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_cp_multi_not_dir.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_cp_multi_not_dir.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_cp_dir_over_file.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_cp_dir_over_file.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_cp_option.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_cp_option.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_mv_missing.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_mv_missing.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_mv_no_dest.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_mv_no_dest.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_mv_no_args.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_mv_no_args.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_mv_into_self.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_mv_into_self.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_mv_same.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_mv_same.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_mv_root.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_mv_root.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_mv_no_parent.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_mv_no_parent.emu
echo "exit code: $?"
echo
echo "$ python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_mv_dir_over_file.emu"
python3 emulator.py --headless --vfs vfs/deep.csv --script scripts/err_mv_dir_over_file.emu
echo "exit code: $?"
echo
