# PyProtect Deploy Mode (-d) - Complete Guide

## What is Deploy Mode?

Deploy mode (`-d` or `--deploy`) protects your code and automatically replaces the original with the protected version, while keeping a timestamped backup in the same location.

## Basic Usage

```bash
pyprotect -d -i /path/to/your/code
```

Or with machine binding:

```bash
pyprotect -d -i /path/to/your/code -b -e 365
```

## How It Works

### Step-by-Step Process

1. **Protection Phase**
   - PyProtect obfuscates your code
   - Protected version is created in a temporary location
   - Shows completion message

2. **Confirmation Phase**
   - Displays what will happen:
     ```
     ============================================================
     🚀 Deploy Mode: Ready to backup and replace
     ============================================================
     📂 Original: /path/to/your/code
     📦 Backup will be: /path/to/your/code.backup_20251209_125530
     ✨ Protected code at: /tmp/protected_code
     
     ⚠️  Proceed with backup and replacement? (y/n):
     ```
   - You must answer **y** or **n**

3. **Deployment Phase** (if you answer 'y')
   - Creates timestamped backup of original
   - Moves protected version to original location
   - Removes temporary files
   - Shows success message with restore command

## Real Example: Deploying Odoo Module

### Before Deploy
```
/odoo18/custom/SCR-18/
├── dtr_jasper/                    # Original code
│   ├── __init__.py
│   ├── models/
│   ├── views/
│   └── ...
├── dtr_stock_form/
└── ...
```

### Run Deploy Command
```bash
cd /odoo18
python3 PyProtect/pyprotect.py -d -i /odoo18/custom/SCR-18/dtr_jasper -b -e 365
```

### Output During Process
```
🏗️  Directory obfuscation mode
==================================================
🔓 Public API preservation: ENABLED (Odoo/Framework compatible)

🔍 Scanning directory: /odoo18/custom/SCR-18/dtr_jasper
📁 Output directory: /odoo18/custom/SCR-18/dtr_jasper

📋 Found 45 total files:
   • 23 Python files to obfuscate
   • 22 other files to copy

🔧 Obfuscating: models/jasper_report.py
   ✅ models/jasper_report.py
🔧 Obfuscating: __init__.py
   ✅ __init__.py
... (processing all files) ...

🎉 Directory processing complete!
   📊 Python files obfuscated: 23/23
   📄 Other files copied: 22/22
   📦 Total files processed: 45/45
   🔒 Machine binding: ENABLED (ID: 0a3a756bffd5...)
   ⏰ License expires: Mon Jan  8 12:55:30 2026

✅ Directory obfuscation complete!

============================================================
🚀 Deploy Mode: Ready to backup and replace
============================================================
📂 Original: /odoo18/custom/SCR-18/dtr_jasper
📦 Backup will be: /odoo18/custom/SCR-18/dtr_jasper.backup_20251209_125530
✨ Protected code at: /odoo18/PyProtect/dist/dtr_jasper

⚠️  Proceed with backup and replacement? (y/n): y

🔄 Deploying...
✅ Original backed up to: /odoo18/custom/SCR-18/dtr_jasper.backup_20251209_125530
✅ Protected version deployed to: /odoo18/custom/SCR-18/dtr_jasper

💡 To restore: mv /odoo18/custom/SCR-18/dtr_jasper.backup_20251209_125530 /odoo18/custom/SCR-18/dtr_jasper

⚠️  WARNING: All code is now bound to the current machine!
   Only machines with Machine ID '0a3a756bffd5...' can run it.
   License expires in 365 days.
```

### After Deploy
```
/odoo18/custom/SCR-18/
├── dtr_jasper/                              # Protected code ✅
│   ├── __init__.py                         # (obfuscated)
│   ├── models/                             # (obfuscated)
│   ├── views/                              # (copied as-is)
│   ├── project.license                     # (license file)
│   └── ...
├── dtr_jasper.backup_20251209_125530/      # Original backup 📦
│   ├── __init__.py                         # (original)
│   ├── models/                             # (original)
│   ├── views/                              # (original)
│   └── ...
├── dtr_stock_form/
└── ...
```

## What Gets Backed Up?

Deploy mode backs up **everything** in the original location:

✅ **All Python files** (`.py`)  
✅ **All other files** (`.xml`, `.js`, `.css`, `.png`, etc.)  
✅ **All subdirectories** (complete directory structure)  
✅ **All permissions** (file permissions are preserved)

## What Gets Replaced?

The original location is completely replaced with:

✅ **Obfuscated Python files** (protected code)  
✅ **Copied other files** (XML, JS, CSS, images - unchanged)  
✅ **License file** (if machine binding is enabled)  
✅ **Same directory structure** (identical layout)

## Backup Naming Convention

Backups use this format:

**For directories:**
```
{original_name}.backup_{YYYYMMDD}_{HHMMSS}
```

**For files:**
```
{original_name}.backup_{YYYYMMDD}_{HHMMSS}{extension}
```

**Examples:**
- `dtr_jasper.backup_20251209_125530/`
- `script.backup_20251209_130045.py`
- `config.backup_20251208_103000.json`

## Command Options

### Basic Deploy
```bash
pyprotect -d -i /path/to/code
# No machine binding, default 365-day license
```

### Deploy with Machine Binding
```bash
pyprotect -d -i /path/to/code -b
# Binds to current machine, 365-day license
```

### Deploy with Custom Expiration
```bash
pyprotect -d -i /path/to/code -b -e 90
# Binds to current machine, 90-day license
```

### Deploy Single File
```bash
pyprotect -d -i /path/to/script.py -b -e 365
# Also works for single files!
```

## Important Notes

### ⚠️ Deploy Mode Behavior

1. **Ignores `-o` flag** - Output is always the same as input location
2. **Requires confirmation** - Always asks y/n before replacing
3. **Atomic operation** - Backup first, then replace (safe)
4. **Timestamp unique** - Each backup has unique timestamp
5. **No auto-cleanup** - Old backups stay until manually deleted

### ⚠️ Before Deploy

✅ **Test first** - Use normal mode (`-o`) to test protection  
✅ **Check space** - Ensure enough disk space for backup  
✅ **Review files** - Know what will be replaced  
✅ **Have rollback plan** - Know how to restore if needed  
✅ **Backup critical data** - Additional backup never hurts

### ⚠️ After Deploy

✅ **Test immediately** - Verify protected code works  
✅ **Check license** - Use `pyprotect -c` to verify license  
✅ **Document deployment** - Note date and backup location  
✅ **Keep backup safe** - Don't delete backup too soon  
✅ **Monitor application** - Watch for any issues

## Answering 'y' (Yes)

When you answer **y**:

✅ Original is moved to `{name}.backup_{timestamp}`  
✅ Protected code is moved to original location  
✅ You can now run your application (protected)  
✅ Backup is available for restore  

**Result:** Original replaced with protected version

## Answering 'n' (No)

When you answer **n**:

✅ Original stays in place (untouched)  
✅ Protected code stays in temp location  
✅ Nothing is changed  
✅ You can test or deploy manually later  

**Result:** Nothing changed, safe to exit

## Restore from Backup

If you need to restore the original:

### Easy Way (Recommended)
```bash
pyprotect -r /path/to/backup.backup_20251209_125530
```

### Manual Way
```bash
cd /odoo18/custom/SCR-18
rm -rf dtr_jasper
mv dtr_jasper.backup_20251209_125530 dtr_jasper
```

## Complete Workflow Example

### 1. Test Protection First
```bash
# Test in /tmp first
pyprotect -i /odoo18/custom/SCR-18/dtr_jasper -o /tmp/test_protected -b -e 365

# Test the protected version
cd /tmp/test_protected
# ... test your module ...
```

### 2. Deploy to Production
```bash
# If test passed, deploy
pyprotect -d -i /odoo18/custom/SCR-18/dtr_jasper -b -e 365
# Answer 'y' when prompted
```

### 3. Verify Deployment
```bash
# Check license
pyprotect -c /odoo18/custom/SCR-18/dtr_jasper

# Restart Odoo and test
sudo systemctl restart odoo
# ... test functionality ...
```

### 4. Rollback if Needed
```bash
# If issues found
pyprotect -r /odoo18/custom/SCR-18/dtr_jasper.backup_20251209_125530
# Answer 'y' to restore
```

## Multi-Module Deployment

Deploy multiple modules one by one:

```bash
# Module 1
pyprotect -d -i /odoo18/custom/SCR-18/dtr_jasper -b -e 365

# Module 2
pyprotect -d -i /odoo18/custom/SCR-18/dtr_stock_form -b -e 365

# Module 3
pyprotect -d -i /odoo18/custom/SCR-18/dtr_sales_form -b -e 365
```

Each module gets its own backup!

## Disk Space Requirements

Deploy mode needs space for:

1. **Original code** (moved to backup)
2. **Protected code** (temporary during processing)
3. **Final protected code** (replaces original)

**Estimate:** 3x the size of your code

**Check before deploy:**
```bash
du -sh /path/to/code           # Check code size
df -h /path/to/parent          # Check available space
```

## Safety Features

✅ **User confirmation** - Won't replace without explicit 'y'  
✅ **Timestamped backups** - Never overwrites existing backups  
✅ **Atomic operations** - Backup first, then replace  
✅ **Clear messaging** - Shows exactly what will happen  
✅ **Error handling** - If deploy fails, backup is preserved  
✅ **Restore command** - Shows how to rollback immediately  

## Troubleshooting

### Deploy Failed
```
❌ Deploy failed: Permission denied
```

**Solution:** Check permissions
```bash
ls -ld /path/to/parent
chmod +w /path/to/code  # if needed
```

### Not Enough Space
```
❌ Deploy failed: No space left on device
```

**Solution:** Free up space or choose different location
```bash
df -h                    # Check space
rm -rf old_backups/      # Remove old backups
```

### Backup Already Exists
This won't happen! Timestamps ensure unique backup names.

But if you manually created a backup with the same name:
```bash
mv existing.backup_20251209_125530 existing.backup_20251209_125530.old
```

## Best Practices

1. ✅ **Always test first** - Use `-o` to test before deploying
2. ✅ **Deploy during maintenance** - Deploy when users aren't active
3. ✅ **One module at a time** - Don't deploy everything at once
4. ✅ **Test immediately** - Verify after each deployment
5. ✅ **Keep backups** - Don't delete backups too soon
6. ✅ **Document deployments** - Keep log of what was deployed when
7. ✅ **Have rollback plan** - Know how to restore quickly
8. ✅ **Monitor logs** - Watch for errors after deployment

## Summary

| Feature | Deploy Mode (`-d`) | Normal Mode (no `-d`) |
|---------|-------------------|----------------------|
| Output location | Same as input | Specified by `-o` |
| Original code | Moved to backup | Untouched |
| Backup | Automatic | Manual |
| Confirmation | Required | Not applicable |
| Use case | Production deployment | Testing, distribution |

Deploy mode is perfect for safely deploying protected code to production with automatic backup and easy rollback! 🚀

