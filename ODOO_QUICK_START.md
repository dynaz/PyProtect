# PyProtect for Odoo - Quick Start Guide

## ✅ Verification Status

PyProtect has been verified to work correctly with the Odoo framework. All compatibility tests pass:

- ✅ Field name detection and preservation
- ✅ Method name pattern recognition  
- ✅ Code structure preservation
- ✅ HTTP Controller handling
- ✅ Manifest file handling

## 🚀 Quick Start

### Protect a Single Odoo Addon

```bash
# Basic protection
python pyprotect.py -i /path/to/my_addon -o dist/my_addon

# With machine binding (license protection)
python pyprotect.py -i /path/to/my_addon -o dist/my_addon -b -e 365

# Deploy mode (backup and replace in-place)
python pyprotect.py -i /path/to/my_addon -d -b
```

### Protect Specific Files

```bash
# Protect a model file
python pyprotect.py -i my_addon/models/sale_order.py -o dist/sale_order.py

# Protect a controller
python pyprotect.py -i my_addon/controllers/main.py -o dist/main.py
```

### Check Machine ID

```bash
# Display current machine ID for licensing
python pyprotect.py -m
```

### Verify License

```bash
# Check license in protected addon
python pyprotect.py -c dist/my_addon/
```

## 📋 What Gets Protected

### ✅ Obfuscated (Safe for Odoo)
- Local variables inside methods
- Private computation logic
- Helper functions (only called locally)
- String literals (when safe)
- Control flow complexity

### ⭐ Preserved (Odoo Compatibility)
- **All class names** (e.g., `SaleOrder`, `AccountMove`)
- **All public methods** (e.g., `action_confirm`, `compute_amount`)
- **All Odoo field names** (e.g., `partner_id`, `amount_total`)
- **Model attributes** (`_name`, `_inherit`, `_order`, etc.)
- **Decorator methods** (`_compute_*`, `_onchange_*`, `_check_*`, etc.)
- **Core ORM methods** (`create`, `write`, `unlink`, `search`, etc.)
- **Special files** (`__manifest__.py`, `__init__.py`)

## 📁 File Structure

After obfuscation:
```
dist/my_addon/
├── __manifest__.py          # Unchanged (required by Odoo)
├── __init__.py              # Unchanged (package init)
├── models/
│   ├── __init__.py          # Unchanged
│   └── sale_order.py        # Obfuscated (with runtime decryption)
├── controllers/
│   ├── __init__.py          # Unchanged
│   └── main.py              # Obfuscated
├── views/
│   └── templates.xml        # Unchanged (not Python)
└── project.license          # License file (if -b used)
```

## 🔒 Machine Binding (Optional)

Machine binding locks the addon to a specific server:

```bash
# Generate license for current machine (365 days)
python pyprotect.py -i my_addon/ -o dist/my_addon/ -b -e 365

# With project URL
python pyprotect.py -i my_addon/ -o dist/my_addon/ -b -u https://github.com/me/addon
```

This creates a `project.license` file that includes:
- Machine ID (hardware fingerprint)
- License key (signed)
- Expiration date
- Protection timestamp

## ⚠️ Important Notes

### DO Obfuscate
✅ Custom addon code you want to protect
✅ Business logic and algorithms
✅ Controllers and routes
✅ Computed fields and methods
✅ Helper functions

### DON'T Obfuscate  
❌ Third-party addons you don't own
❌ Odoo standard modules
❌ Shared libraries used by multiple addons
❌ Open-source community addons

### Automatic Skips
These files are automatically copied without obfuscation:
- `__manifest__.py` / `__openerp__.py`
- `__init__.py` files
- `ir_qweb.py`, `res_lang.py` (complex Odoo core files)
- `assetsbundle.py`, `ir_model.py`, `ir_ui_view.py`

## 🧪 Testing

Always test your obfuscated addon before deployment:

```bash
# 1. Obfuscate to test directory
python pyprotect.py -i my_addon/ -o test/my_addon/

# 2. Copy to Odoo addons path
cp -r test/my_addon /path/to/odoo/addons/

# 3. Update addon list in Odoo
# 4. Install/upgrade the addon
# 5. Test all features thoroughly
```

## 🐛 Troubleshooting

### Error: "Module has no attribute..."
**Cause**: A method or class is being imported but was obfuscated  
**Solution**: The method name should be auto-preserved. Check if it matches Odoo patterns.

### Error: "Invalid field name"
**Cause**: A field name was encrypted  
**Solution**: Field names are auto-detected. Ensure field is defined with `fields.*` syntax.

### Error: Obfuscated code won't import
**Cause**: Syntax error in obfuscated output  
**Solution**: File may have complex f-strings. Add to skip list in `obfuscate_file()`.

### Performance Issues
**Cause**: String decryption overhead  
**Solution**: Minimal impact (< 5%). Decrypt happens once at import time.

## 📊 Performance Impact

- **Import time**: +100-200ms (one-time, at module load)
- **Runtime**: < 5% overhead (negligible)
- **Memory**: +50-100KB per obfuscated file (string storage)

## 🔐 Security Level

PyProtect provides multiple layers of protection:

1. **Variable/Function Obfuscation**: Confusing names (O0O0O, l1l1l, I1I1I)
2. **String Encryption**: Multi-layer XOR + Base64
3. **Control Flow**: Junk code injection
4. **Machine Binding**: Hardware fingerprinting (optional)
5. **License System**: Expiration and validation (optional)

## 💡 Best Practices

1. **Version Control**: Keep original source in Git, never commit obfuscated code
2. **Backup**: PyProtect auto-creates backups, but maintain your own
3. **Testing**: Test obfuscated code thoroughly before production
4. **Documentation**: Document which addons are protected
5. **License Management**: Track machine IDs for customer deployments
6. **Updates**: Re-obfuscate after code changes

## 🆘 Support

For Odoo-specific issues:
1. Run compatibility tests: `python test_odoo_compatibility.py`
2. Check `ODOO_COMPATIBILITY.md` for detailed information
3. Review obfuscation output for warnings
4. Test in development environment first

## 📚 Additional Resources

- `ODOO_COMPATIBILITY.md` - Detailed compatibility documentation
- `test_odoo_compatibility.py` - Test suite
- `pyprotect.py --help` - Command-line options

## ✨ Example Workflow

```bash
# 1. Get current machine ID
python pyprotect.py -m

# 2. Protect addon with license
python pyprotect.py -i my_addon/ -o protected/my_addon/ -b -e 365

# 3. Check license info
python pyprotect.py -c protected/my_addon/

# 4. Test in development
cp -r protected/my_addon /opt/odoo/addons/
# Restart Odoo and test

# 5. Deploy to production
# Copy protected/my_addon to production server
# License is bound to that server's hardware

# 6. For updates: Restore, edit, re-protect
python pyprotect.py -r my_addon.backup_20241211_025730
# Make changes to my_addon/
python pyprotect.py -i my_addon/ -d -b
```

---

**Ready to protect your Odoo addons!** 🛡️

For questions or issues, check the main `ODOO_COMPATIBILITY.md` documentation.

