@echo off
cd /d "%~dp0"
for %%f in (test_*.bat) do (
  echo =============== %%f
  call "%%f"
)
