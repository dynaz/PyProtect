# PyProtect Backup Behavior

## Where Backups Are Created

Backups are **always created in the same directory** as your input file or folder.

## Example 1: Module in /odoo18/custom/SCR-18/

### Input Location
```
/odoo18/custom/SCR-18/dtr_jasper/
```

### After Running Protection
```bash
pyprotect -i /odoo18/custom/SCR-18/dtr_jasper -o /tmp/output
```

### Result
```
/odoo18/custom/SCR-18/
├── dtr_jasper/                              # Original (untouched)
├── dtr_jasper.backup_20251209_125530/       # Backup (same directory) ✅
├── dtr_stock_form/
└── ...

/tmp/output/
└── dtr_jasper/                              # Protected output
```

**Backup is in:** `/odoo18/custom/SCR-18/` (same path as input!)

## Example 2: Deploy Mode

### Input Location
```
/odoo18/custom/SCR-18/dtr_jasper/
```

### After Running Deploy
```bash
pyprotect -d -i /odoo18/custom/SCR-18/dtr_jasper -b -e 365
# Answer 'y' to confirm
```

### Result
```
/odoo18/custom/SCR-18/
├── dtr_jasper/                              # Protected (replaced) ✅
├── dtr_jasper.backup_20251209_125530/       # Input backup (same directory) ✅
├── dtr_jasper.backup_20251209_125531/       # Deploy backup (same directory) ✅
└── ...
```

**Both backups are in:** `/odoo18/custom/SCR-18/` (same path as input!)

## Example 3: Single File

### Input Location
```
/home/user/scripts/my_script.py
```

### After Running Protection
```bash
pyprotect -i /home/user/scripts/my_script.py -o /tmp/protected.py
```

### Result
```
/home/user/scripts/
├── my_script.py                             # Original (untouched)
├── my_script.backup_20251209_125530.py      # Backup (same directory) ✅

/tmp/
└── protected.py                             # Protected output
```

**Backup is in:** `/home/user/scripts/` (same path as input!)

## Backup Path Rules

| Input | Backup Location | Backup Name |
|-------|----------------|-------------|
| `/path/to/module/` | `/path/to/` | `module.backup_YYYYMMDD_HHMMSS/` |
| `/path/to/script.py` | `/path/to/` | `script.backup_YYYYMMDD_HHMMSS.py` |
| `./module/` | `./` (current dir) | `module.backup_YYYYMMDD_HHMMSS/` |

**Key Point:** Backup is always created in the **parent directory** of the input, which keeps it in the same location!

## Finding Your Backups

```bash
# List all backups in the same directory as your module
ls -la /odoo18/custom/SCR-18/*.backup_*

# Example output:
drwxr-xr-x  10 user group  320 Dec  9 12:55 dtr_jasper.backup_20251209_125530
drwxr-xr-x  10 user group  320 Dec  9 13:15 dtr_jasper.backup_20251209_131500
drwxr-xr-x  10 user group  320 Dec  8 10:30 dtr_jasper.backup_20251208_103000
```

## Why This Design?

✅ **Easy to find** - Backup is right next to original  
✅ **No confusion** - Same directory, different name  
✅ **Multiple backups** - Timestamps prevent conflicts  
✅ **Safe restore** - Just rename to restore  
✅ **Clean structure** - Everything in one place

## Complete Example

```bash
# Starting point
/odoo18/custom/SCR-18/
└── dtr_jasper/                    # Your module

# Run protection
cd /odoo18
pyprotect -d -i /odoo18/custom/SCR-18/dtr_jasper -b -e 365 -u https://github.com/dynaz/PyProtect

# After completion
/odoo18/custom/SCR-18/
├── dtr_jasper/                              # Protected version ✅
│   ├── models/
│   ├── views/
│   └── project.license                      # License with URL ✅
└── dtr_jasper.backup_20251209_125530/       # Original backup ✅
    ├── models/
    └── views/
```

**Everything is in the same directory!** ✅

This makes it super easy to:
- Find your backups
- Restore if needed  
- Manage multiple versions
- Keep everything organized

Your backups are always in the same place as your original code! 📦

