# PyPI Authentication Fix

## Issue: 403 Forbidden Error

If you're getting a 403 error when uploading to PyPI, try these solutions:

## Solution 1: Use Environment Variables (Recommended)

Set the token as environment variables before uploading:

**PowerShell:**
```powershell
$env:TWINE_USERNAME = "__token__"
$env:TWINE_PASSWORD = "pypi-AgEIcHlwaS5vcmcCJGViOGMxNDM0LTBmM2QtNGZkNS1iM2Y0LTNmZDcxZGE3Y2FlYwACKlszLCI5NmFiYjQ4MS1lYjFiLTRhZGEtYTBkYS1lNDI0MzIxZTQ3NmIiXQAABiDvT3Il1ILCGjBuEnBb-Jn7xva9zAKrzojFAaVCEb1F4w"
python -m twine upload dist/*
```

**Command Prompt:**
```cmd
set TWINE_USERNAME=__token__
set TWINE_PASSWORD=pypi-AgEIcHlwaS5vcmcCJGViOGMxNDM0LTBmM2QtNGZkNS1iM2Y0LTNmZDcxZGE3Y2FlYwACKlszLCI5NmFiYjQ4MS1lYjFiLTRhZGEtYTBkYS1lNDI0MzIxZTQ3NmIiXQAABiDvT3Il1ILCGjBuEnBb-Jn7xva9zAKrzojFAaVCEb1F4w
python -m twine upload dist/*
```

**Linux/macOS:**
```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-AgEIcHlwaS5vcmcCJGViOGMxNDM0LTBmM2QtNGZkNS1iM2Y0LTNmZDcxZGE3Y2FlYwACKlszLCI5NmFiYjQ4MS1lYjFiLTRhZGEtYTBkYS1lNDI0MzIxZTQ3NmIiXQAABiDvT3Il1ILCGjBuEnBb-Jn7xva9zAKrzojFAaVCEb1F4w
python -m twine upload dist/*
```

## Solution 2: Use the Token Script

**PowerShell:**
```powershell
.\publish_with_token.ps1 -Token "pypi-AgEIcHlwaS5vcmcCJGViOGMxNDM0LTBmM2QtNGZkNS1iM2Y0LTNmZDcxZGE3Y2FlYwACKlszLCI5NmFiYjQ4MS1lYjFiLTRhZGEtYTBkYS1lNDI0MzIxZTQ3NmIiXQAABiDvT3Il1ILCGjBuEnBb-Jn7xva9zAKrzojFAaVCEb1F4w"
```

## Solution 3: Check .pypirc Location

The `.pypirc` file should be in your home directory or the project root. Check:

**Windows:**
- `%USERPROFILE%\.pypirc` or `C:\Users\YourUsername\.pypirc`
- Or in project root: `C:\18odoo\PyProtect\.pypirc`

**Linux/macOS:**
- `~/.pypirc`
- Or in project root

## Solution 4: Verify Token

1. Go to https://pypi.org/manage/account/token/
2. Verify your token is active
3. Make sure you're using the correct token (not TestPyPI token for PyPI)

## Solution 5: Check Package Name

Make sure the package name in `pyproject.toml` matches what you're trying to upload:
- Current name: `pyprotect-th`
- If the name is already taken, you'll need to use a different name

## Quick Test

Test authentication without uploading:
```powershell
python -m twine check dist/*
```

If this works, the package is valid. Then try upload with environment variables.

## Common Issues

1. **Token expired**: Generate a new token at https://pypi.org/manage/account/token/
2. **Wrong token**: Make sure you're using the PyPI token, not TestPyPI
3. **Package name taken**: Try a different package name
4. **Token scope**: Make sure your token has upload permissions

---

**Quick Fix Command:**
```powershell
$env:TWINE_USERNAME = "__token__"
$env:TWINE_PASSWORD = "pypi-AgEIcHlwaS5vcmcCJGViOGMxNDM0LTBmM2QtNGZkNS1iM2Y0LTNmZDcxZGE3Y2FlYwACKlszLCI5NmFiYjQ4MS1lYjFiLTRhZGEtYTBkYS1lNDI0MzIxZTQ3NmIiXQAABiDvT3Il1ILCGjBuEnBb-Jn7xva9zAKrzojFAaVCEb1F4w"
python -m twine upload dist/*
```

