@echo off
cd /d "%~dp0.."
echo $ python emulator.py --headless --vfs vfs/no_such.csv
python emulator.py --headless --vfs vfs/no_such.csv
echo exit code: %errorlevel%
echo.
echo $ python emulator.py --headless --vfs vfs/bad/bad_header.csv
python emulator.py --headless --vfs vfs/bad/bad_header.csv
echo exit code: %errorlevel%
echo.
echo $ python emulator.py --headless --vfs vfs/bad/bad_base64.csv
python emulator.py --headless --vfs vfs/bad/bad_base64.csv
echo exit code: %errorlevel%
echo.
echo $ python emulator.py --headless --vfs vfs/bad/bad_type.csv
python emulator.py --headless --vfs vfs/bad/bad_type.csv
echo exit code: %errorlevel%
echo.
echo $ python emulator.py --headless --vfs vfs/bad/bad_columns.csv
python emulator.py --headless --vfs vfs/bad/bad_columns.csv
echo exit code: %errorlevel%
echo.
echo $ python emulator.py --headless --vfs vfs/bad/duplicate.csv
python emulator.py --headless --vfs vfs/bad/duplicate.csv
echo exit code: %errorlevel%
echo.
echo $ python emulator.py --headless --vfs vfs/bad/empty.csv
python emulator.py --headless --vfs vfs/bad/empty.csv
echo exit code: %errorlevel%
echo.
