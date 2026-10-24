@echo off
cd /d "%~dp0.."
echo $ python emulator.py --headless --vfs vfs/several.csv --script scripts/ok_several.emu
python emulator.py --headless --vfs vfs/several.csv --script scripts/ok_several.emu
echo exit code: %errorlevel%
echo.
