@echo off
cd /d "%~dp0.."
echo $ python emulator.py --headless --vfs vfs/minimal.csv --script scripts/ok_small.emu
python emulator.py --headless --vfs vfs/minimal.csv --script scripts/ok_small.emu
echo exit code: %errorlevel%
echo.
