# PyProtect - Windows Installation Guide

This guide provides detailed instructions for installing PyProtect on Windows systems.

## 📋 Prerequisites

Before installing PyProtect, ensure you have:

1. **Python 3.6+** installed from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"
   - Verify: `python --version` in Command Prompt/PowerShell

2. **Git** (optional, for cloning) from [git-scm.com](https://git-scm.com/download/win)
   - Or download ZIP from GitHub

## 🚀 Quick Install

### Method 1: PowerShell (Recommended)

1. **Open PowerShell** (Right-click Start → Windows PowerShell)

2. **Clone or download PyProtect**:
   ```powershell
   git clone https://github.com/dynaz/PyProtect.git
   cd PyProtect
   ```

3. **Run the installer**:
   ```powershell
   .\install.ps1
   ```

4. **Restart your terminal** (important for PATH changes)

5. **Test installation**:
   ```powershell
   pyprotect --help
   ```

### Method 2: Command Prompt

1. **Open Command Prompt** (Press Win+R, type `cmd`)

2. **Clone or download PyProtect**:
   ```cmd
   git clone https://github.com/dynaz/PyProtect.git
   cd PyProtect
   ```

3. **Run the installer**:
   ```cmd
   install.bat
   ```

4. **Restart your terminal** (important for PATH changes)

5. **Test installation**:
   ```cmd
   pyprotect --help
   ```

## 🔧 Manual Installation

If the automatic installers don't work, follow these steps:

### Step 1: Create Wrapper Scripts

**For PowerShell** (recommended), create `pyprotect.ps1`:
```powershell
# PyProtect PowerShell Wrapper
param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Arguments)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pyprotectPath = Join-Path $scriptDir "pyprotect.py"
if (Get-Command python -ErrorAction SilentlyContinue) {
    & python $pyprotectPath $Arguments
} else {
    Write-Error "Python not found"
}
```

**For Command Prompt**, create `pyprotect.bat`:
```batch
@echo off
python "%~dp0pyprotect.py" %*
```

### Step 2: Add to PATH

**Option A: Using GUI**
1. Press Win+Pause → Advanced system settings
2. Click "Environment Variables"
3. Under "User variables", select "Path" → Edit
4. Click "New" and add the full path to PyProtect folder
5. Click OK on all dialogs

**Option B: Using Command Prompt (as Administrator)**
```cmd
setx PATH "%PATH%;C:\path\to\PyProtect"
```

### Step 3: Restart Terminal

Close and reopen your terminal for PATH changes to take effect.

### Step 4: Test

```cmd
pyprotect --help
```

## 🎯 Usage Examples (Windows)

### Protect a Single File
```cmd
pyprotect -i my_script.py -b
```

### Protect a Project Directory
```cmd
pyprotect -i my_project\ -b
```

### Check Machine ID
```cmd
pyprotect -m
```

### Check License Status
```cmd
pyprotect -c
```

### Custom Output Directory
```cmd
pyprotect -i my_script.py -o protected\my_script.py -b
```

## 🐛 Troubleshooting

### Issue: "python is not recognized"
**Solution**: Python is not in PATH. Reinstall Python and check "Add Python to PATH", or add manually.

### Issue: "pyprotect is not recognized"
**Solutions**:
1. Restart your terminal after installation
2. Check if PyProtect directory is in PATH: `echo %PATH%`
3. Use full path: `python C:\path\to\PyProtect\pyprotect.py`
4. Navigate to PyProtect folder and run: `python pyprotect.py`

### Issue: "Execution policy" error in PowerShell
**Solution**: Run PowerShell as Administrator and execute:
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: "Access denied" when modifying PATH
**Solution**: Run Command Prompt or PowerShell as Administrator:
- Right-click → "Run as administrator"

### Issue: Scripts work in PyProtect folder but not elsewhere
**Solution**: PATH not set correctly. Either:
1. Re-run the installer
2. Manually add to PATH (see Step 2 above)
3. Always navigate to PyProtect folder before use

## 🔄 Updating PyProtect

To update to the latest version:

```cmd
cd PyProtect
git pull
install.bat
```

Or with PowerShell:
```powershell
cd PyProtect
git pull
.\install.ps1
```

## 🗑️ Uninstallation

1. Remove PyProtect from PATH:
   - Open Environment Variables
   - Edit "Path" under User variables
   - Remove the PyProtect directory entry

2. Delete the PyProtect folder:
   ```cmd
   rmdir /s C:\path\to\PyProtect
   ```

## 📝 Notes

- **Python Command**: On Windows, use `python` (not `python3`)
- **Path Separators**: Use backslashes `\` or forward slashes `/` in paths
- **Terminal Restart**: Always restart terminal after PATH changes
- **Permissions**: Some operations may require Administrator privileges
- **Virtual Environments**: Works with venv (activate first)

## 💡 Tips for Windows Users

1. **Use PowerShell**: Modern and more powerful than Command Prompt
2. **Windows Terminal**: Consider using [Windows Terminal](https://aka.ms/terminal) for better experience
3. **WSL**: PyProtect also works in Windows Subsystem for Linux
4. **Anaconda**: Works with Anaconda/Miniconda Python distributions

## 🆘 Getting Help

If you encounter issues:
1. Check this troubleshooting guide
2. Open an issue on [GitHub](https://github.com/dynaz/PyProtect/issues)
3. Include:
   - Windows version
   - Python version (`python --version`)
   - Error messages
   - Steps to reproduce

## ✅ Verification Checklist

After installation, verify:
- [ ] Python is installed: `python --version`
- [ ] PyProtect runs: `pyprotect --help`
- [ ] Can check machine ID: `pyprotect -m`
- [ ] Can obfuscate files: `pyprotect -i test.py -b`

---

**Need more help?** See the main [README.md](README.md) for detailed usage information.

