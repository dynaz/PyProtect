# Troubleshooting PyPI Upload 403 Error

## Current Issue
Getting `403 Forbidden - Invalid or non-existent authentication information` when uploading.

## Possible Causes & Solutions

### 1. Token Issues

**Check your token:**
1. Go to https://pypi.org/manage/account/token/
2. Verify the token exists and is active
3. Check the token scope - it needs "Upload packages" permission
4. If expired or invalid, create a new token

**Token format:**
- Should start with `pypi-`
- Should be the full token (not truncated)
- Make sure there are no extra spaces or characters

### 2. Package Name Already Taken

The package name `pyprotect-th` might already be taken on PyPI.

**Check if name is available:**
- Visit: https://pypi.org/project/pyprotect-th/
- If it exists, you need a different name

**Change package name:**
1. Edit `pyproject.toml`: Change `name = "pyprotect-th"` to something unique
2. Edit `setup.py`: Change `name="pyprotect-th"` to match
3. Rebuild: `python -m build`
4. Try uploading again

**Suggested alternative names:**
- `pyprotect-thai`
- `pyprotect-thailand`
- `pyprotect-th-xxx` (add your initials/identifier)
- `pyprotect-advanced`
- `pyprotect-pro`

### 3. Token Permissions

Make sure your token has the right scope:
1. Go to https://pypi.org/manage/account/token/
2. Create a new token with "Entire account" or "Upload packages" scope
3. Copy the new token
4. Use it in the upload command

### 4. Test with Verbose Output

Get more details about the error:
```powershell
$env:TWINE_USERNAME = "__token__"
$env:TWINE_PASSWORD = "your-token-here"
python -m twine upload dist/* --verbose
```

### 5. Test on TestPyPI First

Test your setup on TestPyPI before uploading to production:

1. Get TestPyPI token: https://test.pypi.org/manage/account/token/
2. Upload to TestPyPI:
```powershell
$env:TWINE_USERNAME = "__token__"
$env:TWINE_PASSWORD = "pypi-your-testpypi-token-here"
python -m twine upload --repository testpypi dist/*
```
3. If TestPyPI works, the issue is with your PyPI token
4. If TestPyPI also fails, check package name and token format

### 6. Manual Token Entry

Try entering the token interactively:
```powershell
python -m twine upload dist/*
# When prompted:
# Username: __token__
# Password: pypi-your-token-here
```

## Quick Diagnostic Steps

1. **Verify token is valid:**
   ```powershell
   # Test authentication (won't upload)
   python -m twine check dist/*
   ```

2. **Check package name availability:**
   - Visit https://pypi.org/project/YOUR-PACKAGE-NAME/
   - If page exists, name is taken

3. **Verify token format:**
   - Should be: `pypi-` followed by long string
   - No spaces or line breaks
   - Full token copied correctly

4. **Check token scope:**
   - Token must have upload permissions
   - Account must be verified

## Recommended Next Steps

1. **Verify token at:** https://pypi.org/manage/account/token/
2. **Check package name:** https://pypi.org/project/pyprotect-th/
3. **If name taken:** Change to unique name in `pyproject.toml` and `setup.py`
4. **If token invalid:** Create new token and try again
5. **Test on TestPyPI first** to isolate the issue

## Alternative: Use Different Package Name

If `pyprotect-th` is taken, quickly change it:

**Edit `pyproject.toml`:**
```toml
name = "pyprotect-thai"  # or any unique name
```

**Edit `setup.py`:**
```python
name="pyprotect-thai",  # match the name above
```

**Rebuild and upload:**
```powershell
python -m build
$env:TWINE_USERNAME = "__token__"
$env:TWINE_PASSWORD = "your-token-here"
python -m twine upload dist/*
```

---

**Most likely issue:** Package name `pyprotect-th` is already taken. Try a different name!

