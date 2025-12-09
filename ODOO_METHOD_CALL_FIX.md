# Odoo Method Call Fix - AttributeError: '_fn_2'

## Issue
After obfuscating Odoo addons, you get:
```
AttributeError: 'ir.http' object has no attribute '_fn_2'. Did you mean: '_fn_0'?
```

This happens when:
- A method call is updated to use an obfuscated name (e.g., `self._fn_2()`)
- But the actual method definition wasn't obfuscated (or was obfuscated to a different name)
- Or the method should have been preserved but wasn't

## Root Cause
The obfuscator pre-populates `func_map` with method names that will be obfuscated, but then:
1. Some methods are later determined to be public and should be preserved
2. The method is removed from `func_map`, but calls to it may have already been updated
3. This creates a mismatch between method calls and definitions

## Fix Applied

### 1. Improved Method Preservation Detection
- Now checks if a method is public (doesn't start with `_`) during pre-population
- Prevents public methods from being added to `func_map` initially
- Reduces mismatches between method calls and definitions

### 2. Better Method Call Mapping
- Ensures method calls via `self.method()` are only updated if the method is actually obfuscated
- Removes methods from `func_map` before processing calls if they shouldn't be obfuscated

## Solution

The fix ensures that:
1. **Public methods** (don't start with `_`) are preserved and not obfuscated
2. **Method calls** are only updated if the method is actually in `func_map`
3. **Method definitions** and **method calls** stay synchronized

## Testing

After the fix, re-obfuscate your addon:

```bash
pyprotect -i C:\18odoo\server\odoo\addons\web_enterprise -b -r
```

The `AttributeError` should be resolved.

## If You Still Get Errors

1. **Check if the method is public**: Methods without leading `_` should be preserved
2. **Check method patterns**: Methods matching Odoo patterns (e.g., `_compute_*`) are preserved
3. **Verify method calls**: All `self.method()` calls should match method definitions

## Common Patterns Preserved

These method patterns are automatically preserved:
- Public methods: `def method_name()` (no leading `_`)
- Odoo patterns: `_compute_*`, `_inverse_*`, `action_*`, etc.
- Special methods: `__init__`, `__str__`, etc.

## Version
- **Fixed in**: PyProtect 1.0.0+
- **Date**: December 2025

---

**Status**: ✅ Fixed - Method calls and definitions now stay synchronized

