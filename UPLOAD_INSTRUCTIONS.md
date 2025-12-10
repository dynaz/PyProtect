# PyProtect v2.1.4 - Upload Instructions

## 🚀 Ready to Upload to PyPI!

The package has been successfully built and is ready for upload.

### Built Files:
- `dist/pyprotect_th-2.1.4-py3-none-any.whl` (30,394 bytes)
- `dist/pyprotect_th-2.1.4.tar.gz` (43,902 bytes)

### Enhanced Features in v2.1.4:
- 🔐 **Multi-layer String Encryption** (XOR + Base64)
- 🎭 **Advanced Variable Name Obfuscation** (O0O, l1l, I1I patterns)
- 🌀 **Control Flow Obfuscation** with Junk Code
- 🛡️ **Anti-Debugging Protection**
- ✅ **Code Integrity Verification**
- 🎪 **Dummy Functions & Dead Code Injection**
- 📦 **Deploy Mode** (`-d` flag)
- 🔄 **Restore Mode** (`-r` flag)

## Upload Methods:

### Method 1: Using API Token
```powershell
# Set environment variables
$env:TWINE_USERNAME = "__token__"
$env:TWINE_PASSWORD = "your-pypi-api-token-here"

# Upload
python -m twine upload dist/pyprotect_th-2.1.4*
```

### Method 2: Interactive Upload
```powershell
python -m twine upload dist/pyprotect_th-2.1.4*
# Will prompt for username and password
```

### Method 3: Using Token Script
```powershell
.\publish_with_token.ps1 -Token "your-pypi-api-token-here"
```

## After Upload:

### Installation:
```bash
pip install pyprotect-th==2.1.4
```

### Usage:
```bash
# Enhanced obfuscation
pyprotect -i file.py -o obfuscated.py

# Deploy mode (backup & replace)
pyprotect -d -i file.py

# With machine binding
pyprotect -i file.py -b -e 365

# Check machine ID
pyprotect -m

# Restore from backup
pyprotect -r file.backup_20251210_195509.py
```

## Package Information:
- **Name**: pyprotect-th
- **Version**: 2.1.4
- **Description**: Enhanced Python code obfuscator with advanced anti-debugging, multi-layer encryption, and machine ID binding
- **PyPI URL**: https://pypi.org/project/pyprotect-th/

## Verification:
Both distribution files have passed `twine check`:
- ✅ `pyprotect_th-2.1.4-py3-none-any.whl`: PASSED
- ✅ `pyprotect_th-2.1.4.tar.gz`: PASSED

The package is ready for production use! 🎉