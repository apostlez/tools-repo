@echo off
chcp 65001 > nul
echo ========================================
echo Strategy Testing (Upbit / XRP/KRW / 1m)
echo ========================================
echo.

REM Activate virtual environment
if not exist "venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found!
    echo Please run setup.bat first.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

REM Check if .env file exists
if not exist ".env" (
    echo.
    echo Warning: .env file not found!
    echo Please create .env file with your Binance API keys.
    pause
    exit /b 1
)

echo Running strategy tests...
echo.
python tests\test_strategy.py

echo.
pause
