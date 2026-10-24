@echo off
cd /d "%~dp0.."
echo $ python emulator.py --headless --script scripts/no_such_file.emu
python emulator.py --headless --script scripts/no_such_file.emu
echo exit code: %errorlevel%
echo.
