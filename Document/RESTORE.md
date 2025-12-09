# Restore from Backup (-r / --restore)

## Quick Start

Restore your original code from a backup with one command:

```bash
python3 pyprotect.py -r /path/to/backup.backup_TIMESTAMP
```

## How It Works

The restore mode:

1. **Validates** the backup path exists
2. **Identifies** the original location automatically
3. **Shows** what will happen
4. **Asks** for confirmation (y/n)
5. **Removes** current version
6. **Restores** backup to original location

## Usage Examples

### Restore a Module

```bash
cd /odoo18
python3 PyProtect/pyprotect.py -r /odoo18/custom/SCR-18/dtr_jasper.backup_20251209_125530
```

**Output:**
```
============================================================
🔄 Restore Mode
============================================================
📦 Backup: /odoo18/custom/SCR-18/dtr_jasper.backup_20251209_125530
🎯 Will restore to: /odoo18/custom/SCR-18/dtr_jasper
⚠️  Current version exists and will be REMOVED

⚠️  Proceed with restore? (y/n): y

🔄 Restoring...
✅ Removed current version at: /odoo18/custom/SCR-18/dtr_jasper
✅ Backup restored to: /odoo18/custom/SCR-18/dtr_jasper

💡 Original restored successfully!
```

### Restore a File

```bash
python3 pyprotect.py -r /path/to/script.backup_20251209_130045.py
```

### List Available Backups

```bash
# Find backups in a directory
ls -la /odoo18/custom/SCR-18/*.backup_*

# Output:
# drwxr-xr-x  10 user  group    320 Dec  9 12:55 dtr_jasper.backup_20251209_125530
# drwxr-xr-x  10 user  group    320 Dec  8 10:30 dtr_jasper.backup_20251208_103000
# drwxr-xr-x  10 user  group    320 Dec  7 15:20 dtr_jasper.backup_20251207_152000
```

## What Gets Restored

### From This:
```
/odoo18/custom/SCR-18/
├── dtr_jasper/                              # Protected (current)
├── dtr_jasper.backup_20251209_125530/       # Original (backup)
```

### To This:
```
/odoo18/custom/SCR-18/
├── dtr_jasper/                              # Original (restored) ✅
```

The backup is **moved** (not copied), so it disappears after successful restore.

## Confirmation Prompt

### If Current Version Exists

```
⚠️  Current version exists and will be REMOVED
```

This warns you that the protected version will be deleted.

### If Target is Empty

```
✅ Target location is empty
```

Safe to restore - nothing will be lost.

## Answer Options

### Answer 'y' (Yes)

```
⚠️  Proceed with restore? (y/n): y

🔄 Restoring...
✅ Removed current version at: /odoo18/custom/SCR-18/dtr_jasper
✅ Backup restored to: /odoo18/custom/SCR-18/dtr_jasper

💡 Original restored successfully!
```

- Current version removed
- Backup moved to original location
- Original code is back

### Answer 'n' (No)

```
⚠️  Proceed with restore? (y/n): n

🛑 Restore cancelled by user
```

- Nothing is changed
- Backup stays in place
- Current version unchanged

## Backup Name Format

Backups must follow this naming pattern:

### Directories
```
{original_name}.backup_{YYYYMMDD}_{HHMMSS}

Examples:
- dtr_jasper.backup_20251209_125530
- my_module.backup_20251208_103000
```

### Files
```
{original_name}.backup_{YYYYMMDD}_{HHMMSS}{extension}

Examples:
- script.backup_20251209_125530.py
- config.backup_20251208_103000.json
```

## Original Path Detection

The tool automatically determines the original path:

| Backup | Original |
|--------|----------|
| `dtr_jasper.backup_20251209_125530/` | `dtr_jasper/` |
| `script.backup_20251209_125530.py` | `script.py` |
| `config.backup_20251208_103000.json` | `config.json` |

## Safety Features

✅ **Validates backup exists** - Won't proceed if backup not found  
✅ **Checks backup name format** - Ensures it's a valid backup  
✅ **Shows what will happen** - Clear preview before action  
✅ **Asks for confirmation** - Won't restore without 'y'  
✅ **Atomic operation** - Remove then move (no partial state)  
✅ **Clear feedback** - Shows exactly what was done

## Common Use Cases

### 1. Protected Code Has Issues

```bash
# Something wrong with protected version
python3 pyprotect.py -r /odoo18/custom/SCR-18/dtr_jasper.backup_20251209_125530

# Back to working original
```

### 2. Need to Make Changes

```bash
# Restore original to make changes
python3 pyprotect.py -r dtr_jasper.backup_20251209_125530

# Make your changes
# ... edit files ...

# Re-protect and deploy
python3 pyprotect.py -i dtr_jasper -d
```

### 3. Compare Protected vs Original

```bash
# Keep protected version
# Extract backup to different location
cp -r dtr_jasper.backup_20251209_125530 /tmp/original
cp -r dtr_jasper /tmp/protected

# Compare
diff -r /tmp/original /tmp/protected
```

### 4. Rollback After Testing

```bash
# Protected version deployed
# Tested but didn't work

# Quick rollback
python3 pyprotect.py -r dtr_jasper.backup_20251209_125530
```

## Troubleshooting

### Backup Not Found

```
❌ Backup not found: /path/to/backup
```

**Solution:** Check the path is correct
```bash
ls -la /path/to/parent/*.backup_*
```

### Invalid Backup Name

```
❌ Not a valid backup name: my_folder
   Backup names should match: name.backup_YYYYMMDD_HHMMSS
```

**Solution:** Make sure the backup has the correct timestamp format.

### Restore Failed

```
❌ Restore failed: Permission denied
```

**Solution:** Check permissions
```bash
ls -ld /path/to/backup
chmod +w /path/to/parent  # if needed
```

### Current Version is Important

If you want to keep the current version before restoring:

```bash
# Backup the current version first
mv dtr_jasper dtr_jasper.current_$(date +%Y%m%d_%H%M%S)

# Then restore
python3 pyprotect.py -r dtr_jasper.backup_20251209_125530
```

## Comparison: Restore Methods

| Method | Command | Pros | Cons |
|--------|---------|------|------|
| **-r flag** | `python3 pyprotect.py -r backup/` | Safe, automatic, confirmed | Requires PyProtect |
| **Manual mv** | `rm -rf module && mv backup module` | Direct, no tool needed | Easy to make mistakes |
| **Manual cp** | `rm -rf module && cp -r backup module` | Keeps backup | Uses more disk space |

## Best Practices

1. ✅ **List backups first** - See what's available
2. ✅ **Check dates** - Restore from the right backup
3. ✅ **Read the prompt** - Understand what will be removed
4. ✅ **Test after restore** - Verify it works
5. ✅ **Clean old backups** - Keep disk space manageable

## Complete Workflow Example

```bash
# 1. Check available backups
cd /odoo18/custom/SCR-18
ls -la *.backup_*

# Output:
# dtr_jasper.backup_20251209_125530/  <- Most recent
# dtr_jasper.backup_20251208_103000/

# 2. Restore from most recent
python3 /odoo18/PyProtect/pyprotect.py -r dtr_jasper.backup_20251209_125530

# 3. Confirm when prompted
# ⚠️  Proceed with restore? (y/n): y

# 4. Verify restoration
cd dtr_jasper
ls -la
# Should see original files

# 5. Test the module
# ... restart Odoo, test functionality ...

# 6. If needed, re-protect
cd ..
python3 /odoo18/PyProtect/pyprotect.py -i dtr_jasper -d
```

## Related Commands

```bash
# Protect module (creates backup if using -d)
python3 pyprotect.py -i module -d

# Restore from backup
python3 pyprotect.py -r module.backup_TIMESTAMP

# List backups
ls -la /path/to/parent/*.backup_*

# Remove old backups
rm -rf module.backup_20251201_*

# Check what's currently deployed
head -20 module/__init__.py  # Look for obfuscation markers
```

## When to Use Restore

✅ **Protected code has bugs** - Back to working original  
✅ **Need to make changes** - Edit original, re-protect  
✅ **Testing issues** - Rollback quickly  
✅ **Comparison needed** - Compare original vs protected  
✅ **Before re-protection** - Start fresh from original  
✅ **Production rollback** - Emergency restore

## When NOT to Use Restore

❌ **Making small fixes** - Fix the issue in protected code  
❌ **Regular updates** - Update source, then re-protect  
❌ **No issues** - If protected version works, leave it  
❌ **Just curious** - Use `cp` instead to keep both versions

---

**Remember:** Restore is destructive! The current version will be removed. Always make sure you're restoring the right backup.

