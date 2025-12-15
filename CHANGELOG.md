# PyProtect Changelog

## Version 1.2.0 (December 12, 2025)

### 🐛 Critical Bug Fixes

#### Fix 1: Method Call/Definition Mismatch

**Issue**: Method calls were being obfuscated while their definitions were preserved, causing `AttributeError` at runtime.

**Root Cause**: The `func_map` dictionary was pre-populated with obfuscated names during scanning, but when methods were later determined to be preserved (e.g., class methods), the `func_map` was not updated. This caused `visit_Attribute` to use the wrong (obfuscated) name for method calls.

**Fix**: Added logic in `visit_FunctionDef` to update `func_map` when a method is preserved, ensuring method calls and definitions always match.

**Files Changed**:
- `pyprotect.py` (lines 932-937): Added critical fix to update `func_map` for preserved methods
- `pyprotect.py` (lines 662-665): Added documentation comment explaining pre-population behavior

**Testing**:
- Created comprehensive test suite (`test_fix.py`)
- All tests pass ✅

**Impact**: 
- Prevents `AttributeError` exceptions in obfuscated code
- Ensures method calls always match their definitions
- Backward compatible (doesn't affect already-obfuscated code)

### 📝 Documentation

**New Files**:
- `FIX_DOCUMENTATION.md`: Detailed explanation of the bug and fix
- `test_fix.py`: Automated test suite to verify the fix
- `CHANGELOG.md`: This file

**Updated Files**:
- `fix_protected.py`: Existing post-processing fixer (no changes needed with new fix)

### 🔍 Verification

To verify the fix works:
```bash
cd /odoo18/PyProtect
python3 test_fix.py
```

Expected: `✅ TEST PASSED - All checks successful!`

### 📊 Real-World Impact

**Before Fix** (dtr_jasper module had 9 manual corrections needed):
- jasper_report.py: 5 method call mismatches
- jasperpy.py: 3 property access mismatches  
- mail_template.py: 1 super() call mismatch

**After Fix**: No manual corrections needed for new obfuscations ✅

#### Fix 2: Import Alias Mismatch

**Issue**: Imported module names were obfuscated in code but import statements weren't updated with aliases, causing `NameError`.

**Example Before**:
```python
from reportlab.pdfgen import canvas  # ❌ No alias
c = _x13_y13_z13.Canvas(buffer)  # NameError!
```

**Fix**: Added `visit_ImportFrom()` and `visit_Import()` methods (lines 1290-1330) that automatically create import aliases when names are obfuscated.

**Example After**:
```python
from reportlab.pdfgen import canvas as _x13_y13_z13  # ✅ Alias added
c = _x13_y13_z13.Canvas(buffer)  # Works!
```

**Files Changed**:
- `pyprotect.py` (lines 1290-1330): Added import alias handling

**Real-World Impact**: Fixed 5 files in dtr_taxation module that had this issue.

#### Fix 3: Keyword Argument Name Mismatch

**Issue**: Function parameters were obfuscated but keyword arguments in calls weren't updated, causing `TypeError`.

**Example Before**:
```python
def render_seq(O0O0O0O0O, l1l1l1l1l, I1I1I2I1I):  # Obfuscated params
    pass

render_seq(c, x=10, y=20)  # ❌ TypeError: unexpected keyword argument 'x'
```

**Fix**: Added `visit_keyword()` method (lines 1275-1289) that updates keyword argument names to match obfuscated parameters.

**Example After**:
```python
render_seq(c, l1l1l1l1l=10, I1I1I2I1I=20)  # ✅ Correct!
```

**Files Changed**:
- `pyprotect.py` (lines 1275-1289): Added keyword argument handling

**Real-World Impact**: Fixed 27 function calls across 5 files in dtr_taxation module.

### 📝 Testing

**New Test Suite**: `test_keyword_import_fix.py`
- Tests keyword argument obfuscation
- Tests import alias creation
- Tests combined scenarios
- **Result**: All tests pass ✅

### 📊 Combined Impact

**Before All Fixes** (manual corrections needed):
- dtr_jasper: 9 method call mismatches
- dtr_taxation: 5 import mismatches + 27 keyword argument mismatches
- **Total**: 41 manual fixes required

**After All Fixes**: 0 manual corrections needed ✅

---

## Version 1.1.0 (December 12, 2025)

### Initial release with method call/definition fix

(See Version 1.2.0 for complete fix history)

---

## Version 1.0.0 (Original)

Initial release with:
- Multi-layer string encryption (XOR + Base64)
- Variable name obfuscation
- Control flow obfuscation
- Machine ID binding
- License verification
- Odoo-specific preservation rules
