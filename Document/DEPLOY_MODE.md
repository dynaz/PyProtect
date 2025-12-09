# Deploy Mode (-d / --deploy)

## What is Deploy Mode?

Deploy mode is a convenient way to protect your code and replace the original in one command. It automatically:

1. **Creates a timestamped backup** of your original code
2. **Protects the code** with obfuscation
3. **Replaces the original** with the protected version
4. **Keeps the backup** in the same parent directory

## Usage

### Basic Deploy

```bash
python3 pyprotect.py -i /path/to/module -d
```

### Deploy with Machine Binding

```bash
python3 pyprotect.py -i /path/to/module -d -b -e 365
```

### Real Example: Deploy dtr_jasper

```bash
cd /odoo18
python3 PyProtect/pyprotect.py -i /odoo18/custom/SCR-18/dtr_jasper -d

# Output will show:
# ... obfuscation progress ...
# ✅ Directory obfuscation complete!
# 
# ============================================================
# 🚀 Deploy Mode: Ready to backup and replace
# ============================================================
# 📂 Original: /odoo18/custom/SCR-18/dtr_jasper
# 📦 Backup will be: /odoo18/custom/SCR-18/dtr_jasper.backup_20251209_125530
# ✨ Protected code at: /odoo18/PyProtect/dist/dtr_jasper
# 
# ⚠️  Proceed with backup and replacement? (y/n): y
# 
# 🔄 Deploying...
# ✅ Original backed up to: /odoo18/custom/SCR-18/dtr_jasper.backup_20251209_125530
# ✅ Protected version deployed to: /odoo18/custom/SCR-18/dtr_jasper
# 
# 💡 To restore: mv /odoo18/custom/SCR-18/dtr_jasper.backup_20251209_125530 /odoo18/custom/SCR-18/dtr_jasper
```

**What happens:**

```
📁 Before:
/odoo18/custom/SCR-18/
├── dtr_jasper/          # Original code
├── dtr_jasper_auto_active/
└── ...

🔄 During:
1. Protects code to temporary location
2. Shows confirmation prompt:
   ⚠️  Proceed with backup and replacement? (y/n): 
3. If 'y': Backs up original and replaces
   If 'n': Keeps everything as-is

📁 After (if confirmed):
/odoo18/custom/SCR-18/
├── dtr_jasper/          # Protected code ✅
├── dtr_jasper.backup_20251209_125530/  # Original backup 📦
├── dtr_jasper_auto_active/
└── ...
```

## Advantages

✅ **User confirmation** - Always asks before replacing (y/n) ⭐ NEW  
✅ **One-step deployment** - No need to manually backup and move files  
✅ **Automatic backup** - Original is safely preserved with timestamp  
✅ **Same location** - Backup stays in parent directory for easy access  
✅ **No cleanup needed** - Output is directly in place  
✅ **Safe** - If deploy fails or cancelled, original is preserved

## Backup Naming

Backups use this format:
- **Directory:** `{name}.backup_{timestamp}`
- **File:** `{name}.backup_{timestamp}{extension}`
- **Timestamp:** `YYYYMMDD_HHMMSS`

Examples:
- `dtr_jasper.backup_20251209_125530/`
- `script.backup_20251209_130045.py`

## Restore from Backup

### Easy Way: Use -r Flag ⭐ NEW

```bash
# One command restore
python3 pyprotect.py -r /odoo18/custom/SCR-18/dtr_jasper.backup_20251209_125530

# It will:
# 1. Show what will be restored
# 2. Ask for confirmation (y/n)
# 3. Remove current version
# 4. Restore backup to original location
```

### Manual Way

If you prefer to do it manually:

```bash
# Directory
cd /odoo18/custom/SCR-18
rm -rf dtr_jasper
mv dtr_jasper.backup_20251209_125530 dtr_jasper

# File
cd /path/to/directory
rm script.py
mv script.backup_20251209_125530.py script.py
```

## Deploy Mode vs Normal Mode

| Feature | Normal Mode (-o) | Deploy Mode (-d) |
|---------|-----------------|------------------|
| Output location | Specified by -o | Same as input |
| Backup | Manual | Automatic |
| Backup location | Anywhere | Same parent directory |
| Original code | Untouched | Replaced |
| Use case | Testing, distribution | Production deployment |

## Safety Features

1. **User Confirmation** - Asks y/n before replacing files ⭐ NEW
2. **Timestamped backups** - Never overwrites existing backups
3. **Atomic operations** - Backup first, then replace
4. **Error handling** - If deploy fails, backup is preserved
5. **Clear messages** - Shows backup location and restore command
6. **Cancel option** - If you say 'n', nothing is changed

## Common Workflows

### Development → Production

```bash
# 1. Test protection first (normal mode)
python3 pyprotect.py -i /path/to/module -o /tmp/test_protected

# 2. Verify it works
# ... test the protected code ...

# 3. Deploy to production (deploy mode)
python3 pyprotect.py -i /path/to/module -d -b -e 365
```

### Update Protected Module

```bash
# Protected version is already deployed
# You have changes in a separate working copy

# Deploy new version (creates new backup)
python3 pyprotect.py -i /path/to/working_copy -d
```

## Important Notes

⚠️ **Deploy mode ignores -o flag** - Output is always the same as input location

⚠️ **Backups accumulate** - Old backups are not automatically deleted. Clean them up periodically:

```bash
# List backups
ls -la /path/to/parent/*.backup_*

# Remove old backups (careful!)
rm -rf /path/to/parent/module.backup_20251201_*
```

⚠️ **Test first** - Always test with normal mode (-o) before using deploy mode in production

## Examples

### Protect Multiple Modules

```bash
# Deploy each module separately
python3 pyprotect.py -i /odoo18/custom/SCR-18/dtr_jasper -d
python3 pyprotect.py -i /odoo18/custom/SCR-18/dtr_stock_form -d
python3 pyprotect.py -i /odoo18/custom/SCR-18/dtr_sales_form -d
```

### Deploy with All Options

```bash
python3 pyprotect.py \
  -i /odoo18/custom/SCR-18/dtr_jasper \
  -d \
  -b \
  -e 365
  
# -i: input module
# -d: deploy mode (backup and replace)
# -b: bind to current machine
# -e 365: license expires in 365 days
```

### Dry Run (Test Without Deploy)

```bash
# Use normal mode to test first
python3 pyprotect.py -i /path/to/module -o /tmp/test_output

# Verify the output works
# ... test ...

# Then deploy
python3 pyprotect.py -i /path/to/module -d
```

## What if I Answer 'n'?

If you answer 'n' (no) to the confirmation prompt:

```
⚠️  Proceed with backup and replacement? (y/n): n

🛑 Deploy cancelled by user
📁 Protected files remain at: /odoo18/PyProtect/dist/dtr_jasper
📁 Original untouched at: /odoo18/custom/SCR-18/dtr_jasper

💡 To deploy manually:
   mv /odoo18/custom/SCR-18/dtr_jasper /odoo18/custom/SCR-18/dtr_jasper.backup_20251209_125530
   mv /odoo18/PyProtect/dist/dtr_jasper /odoo18/custom/SCR-18/dtr_jasper
```

**Nothing is changed:**
- ✅ Original code stays in place
- ✅ Protected code remains in output location
- ✅ You can manually deploy later
- ✅ You can test the protected code first

This is useful when:
- You want to test the protected code before deploying
- You want to review the changes
- You're not sure about replacing yet
- You want to deploy at a different time

## Troubleshooting

### Deploy Failed

If deploy fails, the original code is in the backup:

```bash
# Check what happened
ls -la /path/to/parent/

# Restore if needed
mv module.backup_TIMESTAMP module
```

### Permission Issues

```bash
# Make sure you have write permissions
ls -ld /path/to/parent/
chmod +w /path/to/parent/module  # if needed
```

### Disk Space

Deploy mode needs space for:
- Original code (backup)
- Protected code (temporary)
- Final protected code

Ensure you have at least 3x the module size available.

## Best Practices

1. ✅ **Test first** - Use normal mode before deploy
2. ✅ **Verify backups** - Check backup was created successfully
3. ✅ **Clean old backups** - Remove backups older than needed
4. ✅ **Document deployments** - Keep track of when you deployed
5. ✅ **Have restore plan** - Know how to restore if needed

