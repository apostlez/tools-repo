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
if "%~1"=="" (
    python tests\test_strategy.py
) else (
    echo Using CSV file: %~1
    python tests\test_strategy.py "%~1"
)

echo.
echo Generating backtest chart...
python tests\generate_chart.py

if not "%~1"=="" (
    echo.
    echo Generating candlestick chart...
    python tests\chart_from_csv.py "%~1"

    echo.
    echo Generating candlestick chart with BUY/SELL events...
    python tests\chart_from_csv_with_event.py "%~1"
) else (
    echo.
    echo Generating candlestick chart with BUY/SELL events...
    python tests\chart_from_csv_with_event.py
)

echo.
pause
