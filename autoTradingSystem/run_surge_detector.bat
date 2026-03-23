@echo off
REM 급등 종목 감지 스크립트 실행
REM Surging Coins Detector Runner

echo ========================================
echo   실시간 급등 종목 감지 시작
echo ========================================
echo.

REM Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo [Error] 가상환경을 찾을 수 없습니다.
    echo setup.bat를 먼저 실행하세요.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run surging coins detector
python find_surging_coins.py

REM Deactivate when done
deactivate

pause
