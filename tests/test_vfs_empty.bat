@echo off
cd /d "%~dp0.."
echo $ python emulator.py --headless --script scripts/tree.emu
python emulator.py --headless --script scripts/tree.emu
echo exit code: %errorlevel%
echo.
