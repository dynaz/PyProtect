# Odoo Redirect Fix - KeyError: 'active'

## Issue
When using PyProtect on Odoo controllers with redirects (`-r --redirect`), you get:
```
KeyError: 'active'
Access Denied
```

## Root Cause
The `active` field and other common Odoo/HTTP parameters were being obfuscated, causing Odoo to fail when accessing:
- `request.params.get('active')`
- `kwargs.get('active')`
- Model fields like `record.active`
- Route parameters

## Fix Applied

### 1. Added Common Odoo Fields to Reserved List
The following fields are now preserved (not obfuscated):
- `active` - Common Odoo field for active/inactive records
- `name`, `state`, `status`, `sequence` - Common model fields
- `company_id`, `create_date`, `write_date` - Standard Odoo fields
- `request`, `response`, `redirect` - HTTP-related
- `kwargs`, `args`, `session`, `cookies`, `headers` - Controller parameters

### 2. Preserved Common Field Names in String Literals
When used as dictionary keys (e.g., `kwargs.get('active')`), these strings are not encrypted:
- `active`, `name`, `state`, `status`, `sequence`
- `id`, `ids`, `model`, `res_id`, `res_model`
- `redirect`, `type`, `auth`, `methods`
- `db`, `login`, `password`, `token`, `session_id`

## Usage

### Before Fix
```python
# Odoo controller
@http.route('/my/route', type='http', auth='user')
def my_controller(self, **kwargs):
    active = kwargs.get('active')  # ❌ KeyError: 'active' (obfuscated)
    return request.redirect('/other/route?active=' + str(active))
```

### After Fix
```python
# Odoo controller (obfuscated)
@http.route(_decrypt_str('0'), type=_decrypt_str('1'), auth=_decrypt_str('2'))
def my_controller(self, **kwargs):
    active = kwargs.get('active')  # ✅ Works! 'active' preserved
    return request.redirect(_decrypt_str('3') + str(active))
```

## Testing

After obfuscation, test your controllers:

```bash
# Test redirect functionality
curl -X GET "http://your-odoo-server/my/route?active=true"

# Should work without KeyError
```

## Common Odoo Fields Preserved

The following are automatically preserved:
- **Model Fields**: `active`, `name`, `state`, `status`, `sequence`
- **Standard Fields**: `company_id`, `create_date`, `write_date`, `create_uid`, `write_uid`
- **HTTP Fields**: `request`, `response`, `redirect`, `kwargs`, `args`
- **Session Fields**: `session`, `cookies`, `headers`, `params`
- **Auth Fields**: `db`, `login`, `password`, `token`, `session_id`

## If You Still Get Errors

1. **Check if field is in reserved list**: Add it to `odoo_reserved` in `main.py`
2. **Check string literals**: Common field names used as dict keys are preserved
3. **Check route parameters**: Controller route parameters are preserved
4. **Test incrementally**: Obfuscate one controller at a time to isolate issues

## Version
- **Fixed in**: PyProtect 1.0.0+
- **Date**: December 2025

---

**Status**: ✅ Fixed - `active` and common Odoo fields are now preserved

