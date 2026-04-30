@echo off
REM ============================================================
REM  Marp Markdown -> PPTX Builder
REM  Usage:
REM    build_ppt.bat <input.md>          (output: <input>.pptx, .marp suffix stripped)
REM    build_ppt.bat <input.md> <out.pptx>
REM    build_ppt.bat                     (default: developer_in_the_ai_era.v0.2.marp.md)
REM ============================================================
setlocal EnableDelayedExpansion

set "SCRIPT_DIR=%~dp0"

if "%~1"=="" (
    set "INPUT=%SCRIPT_DIR%developer_in_the_ai_era.v0.2.marp.md"
) else (
    set "INPUT=%~1"
)

if not exist "!INPUT!" (
    echo [ERROR] Input file not found: !INPUT!
    exit /b 1
)

if "%~2"=="" (
    for %%F in ("!INPUT!") do (
        set "DIR=%%~dpF"
        set "BASE=%%~nF"
    )
    REM Strip trailing ".marp" from basename if present
    if "!BASE:~-5!"==".marp" set "BASE=!BASE:~0,-5!"
    set "OUTPUT=!DIR!!BASE!.pptx"
) else (
    set "OUTPUT=%~2"
)

echo.
echo === Marp PPTX Builder ===
echo Input : !INPUT!
echo Output: !OUTPUT!
echo.

call npx --yes @marp-team/marp-cli "!INPUT!" --pptx --html --allow-local-files -o "!OUTPUT!"
set "ERR=!ERRORLEVEL!"

if !ERR! neq 0 (
    echo.
    echo [FAILED] Marp returned error code !ERR!
    exit /b !ERR!
)

echo.
echo [DONE] !OUTPUT!
endlocal
