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
$PYPROTECT_PATH = Join-Path $SCRIPT_DIR "pyprotect.py"

# Check if pyprotect.py exists
if (-not (Test-Path $PYPROTECT_PATH)) {
    Write-Host "ERROR: pyprotect.py not found in current directory" -ForegroundColor Red
    exit 1
}

Write-Host "Found pyprotect.py" -ForegroundColor Green

# Create wrapper batch file
$wrapperContent = "@echo off`r`npython `"$PYPROTECT_PATH`" %*"
$wrapperPath = Join-Path $SCRIPT_DIR "pyprotect.bat"
$wrapperContent | Out-File -FilePath $wrapperPath -Encoding ASCII
Write-Host "Created pyprotect.bat wrapper" -ForegroundColor Green

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
Write-Host "IMPORTANT: Restart your terminal to use the pyprotect command" -ForegroundColor Yellow
Write-Host "Or use: python $PYPROTECT_PATH [options]" -ForegroundColor Gray
Write-Host ""
Write-Host "Run pyprotect --help for full documentation" -ForegroundColor Cyan
