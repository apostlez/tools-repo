@echo off
echo ========================================
echo Auto Trading System - Environment Setup
echo ========================================
echo.

set PYTHON_PATH=C:\Users\yunkw\AppData\Local\Programs\Python\Python312\python.exe

REM Check if Python exists
if not exist "%PYTHON_PATH%" (
    echo Error: Python not found at %PYTHON_PATH%
    echo Please check your Python installation path.
    pause
    exit /b 1
)

echo [1/4] Python found: %PYTHON_PATH%
echo.

REM Create virtual environment
echo [2/4] Creating virtual environment...
"%PYTHON_PATH%" -m venv venv
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)
echo Virtual environment created successfully!
echo.

REM Activate virtual environment and install packages
echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)
echo.

REM Upgrade pip
echo [4/4] Installing required packages...
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install required packages
echo Installing packages from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install packages
    pause
    exit /b 1
)
echo.

echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To activate the virtual environment, run:
echo   venv\Scripts\activate
echo.
echo To deactivate, run:
echo   deactivate
echo.
pause
