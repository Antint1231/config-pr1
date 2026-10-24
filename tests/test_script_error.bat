@echo off
cd /d "%~dp0.."
echo $ python emulator.py --headless --script scripts/error.emu
python emulator.py --headless --script scripts/error.emu
echo exit code: %errorlevel%
echo.
