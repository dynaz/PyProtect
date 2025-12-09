# PyProtect Windows Installation Script (PowerShell)

Write-Host "Installing PyProtect for Windows..." -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is required but not found." -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/" -ForegroundColor Yellow
    exit 1
}

# Get the current directory
$SCRIPT_DIR = $PSScriptRoot

# Check for new package structure or old structure
$NEW_STRUCTURE = Test-Path (Join-Path $SCRIPT_DIR "src\pyprotect\cli.py")
$OLD_STRUCTURE = Test-Path (Join-Path $SCRIPT_DIR "pyprotect.py")

if (-not $NEW_STRUCTURE -and -not $OLD_STRUCTURE) {
    Write-Host "ERROR: PyProtect source not found" -ForegroundColor Red
    Write-Host "Expected: src\pyprotect\cli.py or pyprotect.py" -ForegroundColor Yellow
    exit 1
}

if ($NEW_STRUCTURE) {
    Write-Host "Found new package structure (src/pyprotect/)" -ForegroundColor Green
    Write-Host "Package installation will create 'pyprotect' command" -ForegroundColor Gray
} else {
    Write-Host "Found legacy structure (pyprotect.py)" -ForegroundColor Green
    
    # Create wrapper batch file (for Command Prompt) - backward compatibility
    $PYPROTECT_PATH = Join-Path $SCRIPT_DIR "pyprotect.py"
    $batchContent = @"
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
"@
    $batchPath = Join-Path $SCRIPT_DIR "pyprotect.bat"
    $batchContent | Out-File -FilePath $batchPath -Encoding ASCII
    Write-Host "Created pyprotect.bat wrapper (legacy)" -ForegroundColor Green

    # Create PowerShell wrapper (for PowerShell - preferred)
    $psContent = @"
# PyProtect PowerShell Wrapper
param(
    [Parameter(ValueFromRemainingArguments=`$true)]
    [string[]]`$Arguments
)

`$scriptDir = Split-Path -Parent `$MyInvocation.MyCommand.Path
`$pyprotectPath = Join-Path `$scriptDir "pyprotect.py"

# Try to find Python
`$pythonCmd = `$null

# Try py launcher first
if (Get-Command py -ErrorAction SilentlyContinue) {
    `$pythonCmd = "py"
}
# Then try python
elseif (Get-Command python -ErrorAction SilentlyContinue) {
    `$pythonCmd = "python"
}
# Then try python3
elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    `$pythonCmd = "python3"
}
else {
    Write-Error "ERROR: Python not found. Please ensure Python is installed and in PATH."
    exit 1
}

# Run pyprotect.py with arguments
& `$pythonCmd `$pyprotectPath `$Arguments
"@
    $psPath = Join-Path $SCRIPT_DIR "pyprotect.ps1"
    $psContent | Out-File -FilePath $psPath -Encoding UTF8
    Write-Host "Created pyprotect.ps1 wrapper (legacy)" -ForegroundColor Green
}

# Try to add to user PATH
Write-Host ""
Write-Host "Setting up global access..." -ForegroundColor Yellow

$currentUserPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($currentUserPath -notlike "*$SCRIPT_DIR*") {
    try {
        $newPath = $currentUserPath + ";" + $SCRIPT_DIR
        [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
        Write-Host "Added PyProtect to user PATH" -ForegroundColor Green
        Write-Host "Location: $SCRIPT_DIR" -ForegroundColor Gray
        Write-Host "IMPORTANT: Please restart your terminal for PATH changes to take effect" -ForegroundColor Yellow
    } catch {
        Write-Host "Could not modify PATH automatically" -ForegroundColor Yellow
        Write-Host "You can add it manually to your PATH:" -ForegroundColor Gray
        Write-Host "$SCRIPT_DIR" -ForegroundColor Gray
    }
} else {
    Write-Host "PyProtect directory already in PATH" -ForegroundColor Green
}

# Install Python dependencies if requirements.txt exists
if (Test-Path (Join-Path $SCRIPT_DIR "requirements.txt")) {
    Write-Host ""
    Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
    python -m pip install -r (Join-Path $SCRIPT_DIR "requirements.txt") --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Dependencies installed" -ForegroundColor Green
    }
}

# Install as pip package if setup.py exists
if (Test-Path (Join-Path $SCRIPT_DIR "setup.py")) {
    Write-Host ""
    Write-Host "Installing as Python package..." -ForegroundColor Yellow
    python -m pip install -e $SCRIPT_DIR
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Package installed" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Installation complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Usage Examples:" -ForegroundColor Cyan
Write-Host "  pyprotect -i file.py -b" -ForegroundColor White
Write-Host "  pyprotect -i project\ -b" -ForegroundColor White
Write-Host "  pyprotect -m  # Check machine ID" -ForegroundColor White
Write-Host "  pyprotect -c  # Check license status" -ForegroundColor White
Write-Host ""
if ($NEW_STRUCTURE) {
    Write-Host "IMPORTANT: Restart your terminal to use the pyprotect command" -ForegroundColor Yellow
    Write-Host "The 'pyprotect' command will be available after package installation" -ForegroundColor Gray
} else {
    Write-Host "IMPORTANT: Restart your terminal to use the pyprotect command" -ForegroundColor Yellow
    Write-Host "Or use: python pyprotect.py [options]" -ForegroundColor Gray
}
Write-Host ""
Write-Host "Run pyprotect --help for full documentation" -ForegroundColor Cyan
