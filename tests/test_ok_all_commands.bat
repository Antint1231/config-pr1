@echo off
cd /d "%~dp0.."
echo $ python emulator.py --headless --vfs vfs/deep.csv --script scripts/ok.emu
python emulator.py --headless --vfs vfs/deep.csv --script scripts/ok.emu
echo exit code: %errorlevel%
echo.
