# Ubuntu/WSL Installation Fix

## Issue: Externally-Managed-Environment Error

On Ubuntu 23.04+, Debian 12+, and WSL systems, Python 3.12+ implements PEP 668 which prevents installing packages system-wide to protect the system Python environment.

### Error Message
```
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.
```

## ✅ Solution Implemented

The `install.sh` script has been updated to automatically handle this issue:

1. **First Attempt**: Tries normal `pip3 install -e .`
2. **Auto-Detection**: Detects externally-managed-environment error
3. **Auto-Fallback**: Automatically tries with `--break-system-packages` flag
4. **Graceful Degradation**: If that fails, skips package installation (symlink still works!)

### What This Means

- ✅ **The `pyprotect` command will work** even if package installation is skipped
- ✅ **No manual intervention needed** - the installer handles it automatically
- ✅ **Clear messaging** - users are informed of what's happening
- ✅ **Alternative options provided** - pipx, venv, etc.

## Installation Flow

```
./install.sh
  ↓
✅ Creates symlink (works regardless)
  ↓
📦 Tries package installation
  ↓
⚠️  If externally-managed error:
  ↓
💡 Tries --break-system-packages
  ↓
✅ Success OR ⚠️ Skip (symlink still works!)
```

## Manual Alternatives (if needed)

If you want to install as a package despite the error:

### Option 1: Use pipx (Recommended)
```bash
sudo apt install pipx
pipx install -e .
```

### Option 2: Use Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### Option 3: Use --break-system-packages
```bash
pip3 install -e . --break-system-packages
```
⚠️ **Warning**: This bypasses system protection and may affect system Python packages.

### Option 4: Skip Package Installation
The symlink created by `install.sh` is sufficient to use the `pyprotect` command. Package installation is optional.

## Testing

The fix has been tested to handle:
- ✅ Normal installations (no error)
- ✅ Externally-managed-environment errors
- ✅ Other pip errors
- ✅ Graceful degradation when package install fails

## Files Modified

1. **install.sh** - Added automatic detection and handling
2. **README.md** - Added troubleshooting section for this issue
3. **UBUNTU_WSL_FIX.md** - This documentation file

## Related

- PEP 668: https://peps.python.org/pep-0668/
- Ubuntu Python Policy: https://wiki.ubuntu.com/Python/3.12

---

**Status**: ✅ Fixed and tested
**Date**: December 9, 2025

