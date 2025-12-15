# PyProtect Fix Documentation

## Issue: Method Call/Definition Mismatch

### Problem Description

The PyProtect obfuscator had a critical bug where method **calls** were being obfuscated while method **definitions** were preserved. This caused `AttributeError` exceptions at runtime.

**Example of the bug:**
```python
# Original code
class MyClass:
    def check_jasper_file(self):
        return "checked"
    
    def show_report(self):
        self.check_jasper_file()  # This is a method call
```

**Buggy obfuscated output:**
```python
class MyClass:
    def check_jasper_file(self):  # Definition preserved (correct)
        return "checked"
    
    def show_report(self):
        self.fn_I1I2I1I()  # Call obfuscated (WRONG!)
```

This caused: `AttributeError: 'MyClass' object has no attribute 'fn_I1I2I1I'`

### Root Cause

The obfuscator had two phases:

1. **Pre-population phase**: Scanned all methods and pre-populated `func_map` with obfuscated names for methods that appeared to need obfuscation.

2. **Visit phase**: During `visit_FunctionDef`, the code determined if a method should actually be preserved (e.g., class methods, Odoo reserved methods). However, when a method was preserved, it only updated `var_map` but **not** `func_map`.

3. **Attribute access phase**: During `visit_Attribute`, when encountering `self.method_name()`, the code checked `func_map` and found the pre-populated obfuscated name, causing the method call to be incorrectly obfuscated.

### The Fix

**Location**: `/odoo18/PyProtect/pyprotect.py`, lines 932-937

**What was changed:**

Added a critical check in `visit_FunctionDef` that updates `func_map` when a method is preserved:

```python
# BEFORE (buggy):
else:
    # Function is preserved - make sure var_map knows about it
    if node.name not in self.var_map:
        self.var_map[node.name] = node.name

# AFTER (fixed):
else:
    # Function is preserved - make sure both var_map and func_map know about it
    if node.name not in self.var_map:
        self.var_map[node.name] = node.name
    # CRITICAL FIX: If the method was pre-populated in func_map but we're now preserving it,
    # we need to update func_map to map the method name to itself.
    # This ensures that method calls via attributes (self.method_name()) use the correct name.
    if node.name in self.func_map and self.func_map[node.name] != node.name:
        # Method was pre-populated with obfuscated name but should be preserved
        self.func_map[node.name] = node.name
```

### Impact

This fix ensures that:
1. When a method definition is preserved, its entry in `func_map` is updated to map to itself
2. When `visit_Attribute` encounters a method call, it will use the correct (preserved) name
3. Method calls and definitions always match

### Testing

A comprehensive test script (`test_fix.py`) was created that:
- Creates test classes with methods that should be preserved
- Runs PyProtect on the test code
- Verifies that method definitions are preserved
- Verifies that no obfuscated method calls exist
- Executes the obfuscated code to ensure it works correctly

**Test result**: ✅ All tests pass

### Files Fixed in dtr_jasper Module

After applying this fix to PyProtect, the following files in the dtr_jasper module were manually corrected:

1. **jasper_report.py** (5 fixes):
   - `self.func_O0O0O0O()` → `self.hash_md5()`
   - `self.method_l1l1l1l()` → `self.active()`
   - `self.fn_I1I2I1I()` → `self.check_jasper_file()`
   - `self.handler_E4()` → `self.write_file_to_field()`
   - `self._exec_3_6()` → `self.clean_up_temp()`

2. **jasperpy.py** (3 fixes):
   - `self.fn_I1I2I1I` → `self.command` (property access, 3 occurrences)

3. **mail_template.py** (1 fix):
   - `super().func_O0O0O0O()` → `super().generate_email()`

### Prevention

With this fix in place, future obfuscation runs will not produce method call/definition mismatches. The obfuscator now correctly handles:

- Class methods (always preserved)
- Module-level functions (always preserved)
- Odoo reserved methods (always preserved)
- Methods with special decorators (e.g., `@api.autovacuum`, `@api.cron`)
- Property accessors (e.g., `self.command` where `command` is a `@property`)

### Verification

To verify the fix works on your code:

```bash
cd /odoo18/PyProtect
python3 test_fix.py
```

Expected output: `✅ TEST PASSED - All checks successful!`

### Additional Notes

- The fix is backward compatible and doesn't affect already-obfuscated code
- The fix only affects the obfuscation process going forward
- Already-obfuscated files with mismatches need to be manually corrected or re-obfuscated
- The pre-population phase is still useful for performance and consistency, but now has proper correction logic

## Additional Fixes Applied (December 12, 2025)

### Fix 2: Import Alias Mismatch

**Problem**: When imported module names were obfuscated in the code but not aliased in the import statement.

**Example**:
```python
# Import statement (not updated):
from reportlab.pdfgen import canvas

# Code using obfuscated name:
c = _x13_y13_z13.Canvas(buffer)  # ❌ NameError: '_x13_y13_z13' is not defined
```

**Solution**: Added `visit_ImportFrom()` and `visit_Import()` methods that automatically create import aliases when the imported name is obfuscated:

```python
def visit_ImportFrom(self, node):
    """Handle import statements to create aliases when imported names are obfuscated"""
    if node.names:
        for alias in node.names:
            import_name = alias.name
            if import_name in self.var_map and self.var_map[import_name] != import_name:
                if not alias.asname:
                    alias.asname = self.var_map[import_name]
    return node
```

**Result**: Import statements now automatically get aliases:
```python
from reportlab.pdfgen import canvas as _x13_y13_z13  # ✅ Correct!
```

### Fix 3: Keyword Argument Name Mismatch

**Problem**: Function parameters were obfuscated but keyword arguments in function calls were not updated.

**Example**:
```python
# Function definition (obfuscated):
def render_seq(O0O0O0O0O, l1l1l1l1l, I1I1I2I1I):  # originally (canvas, x, y)
    pass

# Function call (not updated):
render_seq(c, x=10, y=20)  # ❌ TypeError: got an unexpected keyword argument 'x'
```

**Solution**: Added `visit_keyword()` method that updates keyword argument names to match obfuscated parameters:

```python
def visit_keyword(self, node):
    """Handle keyword arguments in function calls"""
    if node.arg and node.arg in self.var_map:
        node.arg = self.var_map[node.arg]
    self.generic_visit(node)
    return node
```

**Result**: Keyword arguments now use obfuscated names:
```python
render_seq(c, l1l1l1l1l=10, I1I1I2I1I=20)  # ✅ Correct!
```

### Testing

Created comprehensive test suite (`test_keyword_import_fix.py`) that verifies:
- ✅ Keyword arguments are correctly updated
- ✅ Import aliases are automatically created
- ✅ Combined scenarios work correctly
- ✅ Obfuscated code executes without errors

**All tests pass!** 🎉

## Date

Fixes applied: December 12, 2025

