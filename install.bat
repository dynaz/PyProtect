@echo off
REM PyProtect Windows Installation Script (Batch)

echo.
echo 🚀 Installing PyProtect for Windows...
echo =======================================
echo.

REM Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not found.
    echo    Please install Python from https://www.python.org/
    exit /b 1
)

python --version
echo ✅ Python found
echo.

REM Get the current directory
set "SCRIPT_DIR=%~dp0"
set "PYPROTECT_PATH=%SCRIPT_DIR%pyprotect.py"

REM Check if pyprotect.py exists
if not exist "%PYPROTECT_PATH%" (
    echo ❌ pyprotect.py not found in current directory
    exit /b 1
)

echo ✅ Found pyprotect.py
echo.

REM Create wrapper batch file
echo @echo off > "%SCRIPT_DIR%pyprotect.bat"
echo python "%PYPROTECT_PATH%" %%* >> "%SCRIPT_DIR%pyprotect.bat"
echo ✅ Created pyprotect.bat wrapper
echo.

REM Add to PATH (using setx)
echo Setting up global access...
setx PATH "%PATH%;%SCRIPT_DIR%" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Could not modify PATH automatically
    echo    You can add it manually to your PATH:
    echo    %SCRIPT_DIR%
) else (
    echo ✅ Added PyProtect to user PATH
    echo    Location: %SCRIPT_DIR%
    echo ⚠️  Please restart your terminal for PATH changes to take effect
)
echo.

REM Install Python dependencies if requirements.txt exists
if exist "%SCRIPT_DIR%requirements.txt" (
    echo Installing Python dependencies...
    python -m pip install -r "%SCRIPT_DIR%requirements.txt" --quiet
    if errorlevel 0 (
        echo ✅ Dependencies installed
    )
    echo.
)

REM Install as pip package if setup.py exists
if exist "%SCRIPT_DIR%setup.py" (
    echo 📦 Installing as Python package...
    python -m pip install -e "%SCRIPT_DIR%"
    if errorlevel 0 (
        echo ✅ Package installed
    )
    echo.
)

echo.
echo 🎉 Installation complete!
echo.
echo 📖 Usage Examples:
echo   pyprotect -i file.py -b
echo   pyprotect -i project\ -b
echo   pyprotect -m  # Check machine ID
echo   pyprotect -c  # Check license status
echo.
echo ⚠️  IMPORTANT: Restart your terminal to use 'pyprotect' command
echo    Or use: python "%PYPROTECT_PATH%" [options]
echo.
echo 📖 Run 'pyprotect --help' for full documentation
echo.
pause

