@echo off
REM PyProtect wrapper - tries multiple methods to find Python
setlocal enabledelayedexpansion

REM Try py launcher first
py "%~dp0pyprotect.py" %* 2>nul
if %errorlevel% equ 0 exit /b 0

REM Try python command
python "%~dp0pyprotect.py" %* 2>nul
if %errorlevel% equ 0 exit /b 0

REM Try python3 command
python3 "%~dp0pyprotect.py" %* 2>nul
if %errorlevel% equ 0 exit /b 0

REM If all fail, show error
echo ERROR: Python not found. Please ensure Python is installed and in PATH.
echo.
echo You can also run directly: python "%~dp0pyprotect.py" [options]
exit /b 1
