# PyProtect PyPI Publishing Script (PowerShell)

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
Write-Host "Built files:" -ForegroundColor Cyan
Get-ChildItem dist\ | Format-Table Name, Length -AutoSize

# Ask for confirmation
Write-Host ""
$confirm = Read-Host "Upload to PyPI? (y/N)"
if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-Host "Upload cancelled" -ForegroundColor Yellow
    exit 0
}

# Upload to PyPI
Write-Host ""
Write-Host "Uploading to PyPI..." -ForegroundColor Yellow
python -m twine upload dist/*

Write-Host ""
Write-Host "Successfully published to PyPI!" -ForegroundColor Green
Write-Host ""
Write-Host "Install with: pip install pyprotect" -ForegroundColor Cyan
Write-Host "View at: https://pypi.org/project/pyprotect/" -ForegroundColor Cyan

