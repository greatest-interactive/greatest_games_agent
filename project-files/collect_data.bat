@echo off
REM Collect Game Market Data - Windows Batch Script
REM This script collects trending game data from all platforms

cd /d "%~dp0"

echo.
echo ============================================================
echo   GREATEST GAME AGENT - DATA COLLECTION
echo ============================================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run collection script
python collect_data.py

REM Keep window open to see results
pause
