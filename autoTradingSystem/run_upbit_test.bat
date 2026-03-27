@echo off
echo ========================================
echo Upbit API Test
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
    echo Please create a .env file with Upbit API keys:
    echo   UPBIT_ACCESS_KEY=your_access_key_here
    echo   UPBIT_SECRET_KEY=your_secret_key_here
    echo.
    echo Upbit API 키 발급: https://upbit.com/mypage/open_api_management
    echo.
    pause
    exit /b 1
)

REM Run the test script
echo Running Upbit API tests...
echo.
python tests\test_upbit_api.py

echo.
pause
