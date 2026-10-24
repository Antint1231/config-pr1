@echo off
cd /d "%~dp0.."
echo $ python emulator.py --headless --script scripts/bad_quote.emu
python emulator.py --headless --script scripts/bad_quote.emu
echo exit code: %errorlevel%
echo.
