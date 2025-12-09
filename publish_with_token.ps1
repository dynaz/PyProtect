# PyProtect PyPI Publishing Script with Token (PowerShell)
# Use this if .pypirc authentication doesn't work

param(
    [Parameter(Mandatory=$false)]
    [string]$Token
)

Write-Host "Publishing PyProtect to PyPI" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if build tools are installed
Write-Host "Checking build tools..." -ForegroundColor Yellow
try {
    python -m build --version | Out-Null
} catch {
    Write-Host "Installing build tools..." -ForegroundColor Yellow
    python -m pip install --upgrade build twine
}

# Clean previous builds
Write-Host "Cleaning previous builds..." -ForegroundColor Yellow
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
Get-ChildItem -Filter "*.egg-info" -Recurse | Remove-Item -Recurse -Force
Write-Host "Cleaned" -ForegroundColor Green

# Build the package
Write-Host ""
Write-Host "Building package..." -ForegroundColor Yellow
python -m build
Write-Host "Build complete" -ForegroundColor Green

# Check the distribution
Write-Host ""
if (Test-Path "dist") {
    Write-Host "Built files:" -ForegroundColor Cyan
    Get-ChildItem dist\ | Format-Table Name, Length -AutoSize
} else {
    Write-Host "ERROR: Build failed - dist directory not found" -ForegroundColor Red
    exit 1
}

# Ask for confirmation
Write-Host ""
$confirm = Read-Host "Upload to PyPI? (y/N)"
if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-Host "Upload cancelled" -ForegroundColor Yellow
    exit 0
}

# Set up authentication
if ($Token) {
    Write-Host ""
    Write-Host "Using provided token..." -ForegroundColor Yellow
    $env:TWINE_USERNAME = "__token__"
    $env:TWINE_PASSWORD = $Token
} else {
    Write-Host ""
    Write-Host "Token not provided. Options:" -ForegroundColor Yellow
    Write-Host "1. Enter token when prompted" -ForegroundColor Cyan
    Write-Host "2. Cancel and run: .\publish_with_token.ps1 -Token 'your-token-here'" -ForegroundColor Cyan
    Write-Host ""
}

# Upload to PyPI
Write-Host ""
Write-Host "Uploading to PyPI..." -ForegroundColor Yellow
python -m twine upload dist/*

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Successfully published to PyPI!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Install with: pip install pyprotect-th" -ForegroundColor Cyan
    Write-Host "View at: https://pypi.org/project/pyprotect-th/" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "Upload failed. Check your token and try again." -ForegroundColor Red
    exit 1
}

