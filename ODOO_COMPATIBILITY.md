# PyProtect - Odoo Framework Compatibility

## Overview

PyProtect has been specifically enhanced to work seamlessly with the Odoo ERP framework. This document outlines the Odoo-specific features and compatibility measures implemented.

## Key Features for Odoo Compatibility

### 1. **Preserved Odoo Patterns**

PyProtect automatically preserves the following Odoo-specific patterns to ensure framework compatibility:

#### Model Attributes
- `_name`, `_description`, `_inherit`, `_inherits`
- `_rec_name`, `_order`, `_sql_constraints`, `_constraints`
- `_auto`, `_table`, `_table_query`, `_sequence`
- `_parent_name`, `_parent_store`, `_date_name`, `_fold_name`
- `_abstract`, `_transient`, `_log_access`, `_check_company_auto`

#### Model Lifecycle Methods
- `_register_hook`, `_setup_complete`, `_constraint_methods`

#### Common ORM Methods
- `create`, `write`, `unlink`, `search`, `browse`, `read`
- `search_read`, `name_get`, `name_search`, `name_create`
- `default_get`, `fields_get`, `fields_view_get`

#### Field Names
All Odoo field definitions using `fields.Char()`, `fields.Many2one()`, etc. are automatically detected and preserved.

### 2. **Preserved Method Name Patterns**

Methods matching these patterns are preserved to maintain Odoo's decorator and callback system:

- **Compute methods**: `_compute_*`, `_compute`
- **Inverse methods**: `_inverse_*`
- **Search methods**: `_search_*`
- **Onchange methods**: `_onchange_*`
- **Constraint methods**: `_constraint_*`, `_check_*`
- **Action methods**: `action_*`, `button_*`
- **Default methods**: `_default_*`
- **Cron/Autovacuum**: `_cron_*`, `_autovacuum`
- **Lifecycle methods**: `_create_*`, `_write_*`, `_update_*`, `_unlink*`
- **Info/Render methods**: `_info`, `_render*`
- **Build/Load/Save**: `_build_*`, `_load_*`, `_save_*`
- **Validation**: `_validate_*`, `_check_*`, `_is_*`, `_has_*`, `_can_*`
- **Processing**: `_process_*`, `_handle_*`, `_execute_*`, `_perform_*`
- **Collection**: `_all_*`, `_collect_*`, `_fetch_*`, `_find_*`
- **Transform**: `_convert_*`, `_parse_*`, `_normalize_*`, `_sanitize_*`
- **Data ops**: `_copy_*`, `_merge_*`, `_split_*`, `_join_*`
- **Functional**: `_map_*`, `_filter_*`, `_reduce_*`
- **Module/XMLID**: `_module_*`, `_xmlid*`, `_inherited*`
- **Routing**: `routing_*`
- **Preparation**: `_prepare_*`

### 3. **HTTP Controller Support**

PyProtect preserves:
- `Controller` class inheritance
- `@route` decorator parameters
- `@http` decorator patterns
- HTTP request/response handling: `request`, `Response`, `session`
- RPC dispatch: `dispatch_rpc`, `service`, `method`

### 4. **API Decorator Compatibility**

All Odoo API decorators are properly handled:
- `@api.model`
- `@api.depends()`
- `@api.constrains()`
- `@api.onchange()`
- `@api.model_create_multi`
- `@api.returns()`
- `@api.autovacuum`
- `@api.ondelete()`
- `@tools.ormcache()` and variants

Field and parameter names referenced in decorator arguments are automatically preserved.

### 5. **Field Name Detection**

PyProtect automatically detects and preserves:
- All field assignments using `fields.*` classes
- Field references in decorator parameters: `compute`, `depends`, `related`, `inverse_name`, etc.
- Related field notation: `partner_id.name`
- Comma-separated dependencies: `'field1, field2'`
- Field suffixes: `_id`, `_ids`, `_line`, `_lines`, etc.

### 6. **Special Files Handling**

The following files are automatically skipped (copied as-is without obfuscation):
- `__manifest__.py` / `__openerp__.py` - Module manifests (Odoo uses `ast.literal_eval`)
- `__init__.py` - Package initialization files
- `ir_qweb.py` - Complex QWeb template rendering with f-strings
- `res_lang.py` - Language/localization handling
- `assetsbundle.py` - Asset bundling with complex string operations
- `ir_model.py` - Model introspection with complex f-strings
- `ir_ui_view.py` - View rendering with complex templates

### 7. **Class and Method Preservation**

- **All class names** are preserved (never obfuscated)
- **All module-level functions** are preserved (can be imported by other modules)
- **All class methods** are preserved (can be called from other modules/addons)
- **Special methods** (`__init__`, `__call__`, etc.) are always preserved
- **Single underscore methods** (`_private_method`) are preserved (Odoo internal API)

### 8. **Parameter Name Handling**

For Odoo compatibility:
- Parameters in class methods are preserved (may be called with keyword arguments)
- `self` and `cls` are always preserved
- Reserved parameter names (`context`, `key`, `keys`, `args`, `kwargs`, etc.) are preserved
- Parameters in special methods are preserved

### 9. **String Encryption with Odoo Safety**

PyProtect's string encryption intelligently skips:
- Field names and model names (e.g., `partner_id`, `res.partner`)
- Database field references
- XML IDs and external identifiers
- Domain expressions
- Python code snippets
- Very long strings (likely templates or code)

This prevents breaking:
- Model and field lookups
- Domain evaluations
- XML ID references
- Template rendering

### 10. **Exception and Error Handling**

Preserved Odoo exception classes:
- `UserError`, `ValidationError`, `AccessError`, `MissingError`
- `AccessDenied`, `RedirectWarning`

### 11. **Cache Support**

Full support for Odoo's caching mechanisms:
- `@tools.ormcache()` decorator
- `@tools.ormcache_context()` decorator
- Parameter names in cache decorators are preserved
- `invalidate_cache` methods preserved

## Usage Examples

### Basic Odoo Module Obfuscation

```bash
# Obfuscate a single Odoo model file
python pyprotect.py -i addon/models/sale_order.py -o dist/sale_order.py

# Obfuscate entire Odoo addon with machine binding
python pyprotect.py -i my_addon/ -o dist/my_addon/ -b -e 365

# Deploy mode: backup and replace in-place
python pyprotect.py -i my_addon/ -d -b
```

### Checking Compatibility

```bash
# Display current machine ID for licensing
python pyprotect.py -m

# Check license status in obfuscated addon
python pyprotect.py -c dist/my_addon/
```

### Advanced Options

```bash
# Full obfuscation (may break some imports - not recommended for Odoo)
python pyprotect.py -i addon/ -o dist/addon/ --no-preserve-api

# With project URL in license
python pyprotect.py -i addon/ -o dist/addon/ -b -u https://github.com/user/addon
```

## Best Practices for Odoo

1. **Test After Obfuscation**: Always test your obfuscated addon in a development environment first

2. **Backup Original**: PyProtect automatically creates backups, but keep your original source in version control

3. **Preserve Public API**: Use default settings (preserve public API) for maximum Odoo compatibility

4. **Machine Binding**: Use `-b` flag for licensing and machine binding to protect your IP

5. **Exclude Sensitive Files**: The obfuscator automatically excludes manifests and init files

6. **Check Dependencies**: If your addon depends on obfuscated code, ensure all references are preserved

7. **Review Logs**: Check the obfuscation output for warnings about skipped files

## What Gets Obfuscated

✅ **Obfuscated (Safe for Odoo):**
- Local variables inside methods
- Private helper functions (only called locally)
- Internal computation logic
- String literals (when safe)
- Control flow complexity

❌ **NOT Obfuscated (Preserved):**
- Class names
- Public methods and module-level functions  
- Odoo field names
- Model attributes (`_name`, `_inherit`, etc.)
- Decorator parameters
- Method names matching Odoo patterns
- Parameter names in class methods
- Reserved Odoo names

## Troubleshooting

### Issue: "AttributeError: module has no attribute..."
**Solution**: The obfuscated module may have an internal function that's imported elsewhere. Add the function name pattern to `odoo_method_patterns` in the script.

### Issue: "KeyError: field name not found"
**Solution**: A field name may have been encrypted. Add it to the field name detection logic or odoo_reserved set.

### Issue: "Cache key mismatch"
**Solution**: Ensure all `@ormcache` parameter names match the actual function parameters. The obfuscator preserves these automatically.

### Issue: Obfuscated code fails with "invalid syntax"
**Solution**: Some files with complex f-strings may need to be added to the skip list (see section 6).

## Technical Details

### How It Works

1. **AST Analysis**: PyProtect parses Python code into an Abstract Syntax Tree
2. **Name Collection**: First pass collects all Odoo field and method names
3. **Selective Obfuscation**: Second pass obfuscates only safe-to-change names
4. **String Encryption**: Encrypts strings that don't break Odoo functionality
5. **Code Generation**: Generates obfuscated code with decryption runtime

### Performance Impact

- **Compile Time**: Slightly slower first load due to string decryption overhead
- **Runtime Performance**: Minimal impact (< 5% overhead) after initial load
- **Memory**: Small increase for encrypted string storage

### Security Level

- **Variable/Function Obfuscation**: Advanced (multiple patterns)
- **String Encryption**: Multi-layer (XOR + Base64)
- **Control Flow**: Junk code injection
- **Machine Binding**: Hardware fingerprinting (optional)
- **Code Integrity**: Hash verification (optional)

## Compatibility Matrix

| Odoo Version | PyProtect Compatibility | Notes |
|--------------|------------------------|-------|
| Odoo 17.x    | ✅ Fully Compatible    | Tested extensively |
| Odoo 16.x    | ✅ Fully Compatible    | All features supported |
| Odoo 15.x    | ✅ Fully Compatible    | All features supported |
| Odoo 14.x    | ✅ Compatible          | Minor API differences |
| Odoo 13.x    | ⚠️ Mostly Compatible   | Some decorators may differ |
| Odoo 12.x and earlier | ⚠️ Limited Support | Manual testing recommended |

## Support and Updates

For Odoo-specific compatibility issues or feature requests, please ensure:
1. You're using the latest version of PyProtect
2. You've preserved the default API preservation settings
3. You've checked that your custom addon follows Odoo conventions

## License and Restrictions

PyProtect is designed to protect your intellectual property while maintaining Odoo framework compatibility. The obfuscated code:
- Can be deployed on customer servers
- Can be licensed per machine with `-b` flag
- Cannot be easily reverse-engineered
- Maintains full Odoo functionality

---

**Note**: This document is specific to Odoo framework compatibility. For general PyProtect usage, see the main README.

