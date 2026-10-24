@echo off
cd /d "%~dp0.."
echo $ python emulator.py --headless --script scripts/ok_empty.emu
python emulator.py --headless --script scripts/ok_empty.emu
echo exit code: %errorlevel%
echo.
