@echo off
echo ========================================
echo Binance API Test - Paper Trading Mode
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
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo Please edit .env file and add your Binance API keys:
    echo   BINANCE_API_KEY=your_api_key_here
    echo   BINANCE_SECRET_KEY=your_secret_key_here
    echo.
    echo For paper trading, use testnet keys from:
    echo   https://testnet.binance.vision/
    echo.
    pause
    exit /b 1
)

REM Run the test script
echo Running Binance API tests...
echo.
python tests\test_binance_api.py

echo.
pause
