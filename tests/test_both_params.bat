@echo off
cd /d "%~dp0.."
echo $ python emulator.py --headless --vfs C:/data/vfs.csv --script scripts/ok.emu
python emulator.py --headless --vfs C:/data/vfs.csv --script scripts/ok.emu
echo exit code: %errorlevel%
echo.
