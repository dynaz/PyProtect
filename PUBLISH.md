# Publishing PyProtect to PyPI

This guide explains how to publish PyProtect to PyPI (Python Package Index).

## Prerequisites

1. **PyPI Account**: Create an account at https://pypi.org/account/register/
2. **API Token**: Generate a token at https://pypi.org/manage/account/token/
3. **Build Tools**: Install build and twine:
   ```bash
   pip install --upgrade build twine
   ```

## Configuration

### 1. Set up PyPI credentials

Your `.pypirc` file has been created with your token. **IMPORTANT**: 
- Never commit `.pypirc` to version control
- Add it to `.gitignore`
- Keep your token secure

### 2. Verify package structure

Ensure your package structure is correct:
```
pyprotect-project/
├── src/
│   └── pyprotect/
│       ├── __init__.py
│       ├── cli.py
│       └── main.py
├── pyproject.toml
├── setup.py
├── README.md
└── LICENSE
```

## Publishing Steps

### Method 1: Using the publish script (Recommended)

#### Linux/macOS:
```bash
chmod +x publish.sh
./publish.sh
```

#### Windows (PowerShell):
```powershell
.\publish.ps1
```

### Method 2: Manual publishing

1. **Clean previous builds**:
   ```bash
   rm -rf dist/ build/ *.egg-info
   ```

2. **Build the package**:
   ```bash
   python -m build
   ```

3. **Check the distribution**:
   ```bash
   ls -lh dist/
   ```
   You should see:
   - `pyprotect-1.0.0.tar.gz` (source distribution)
   - `pyprotect-1.0.0-py3-none-any.whl` (wheel)

4. **Test upload to TestPyPI** (optional but recommended):
   ```bash
   python -m twine upload --repository testpypi dist/*
   ```
   Then test installation:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ pyprotect
   ```

5. **Upload to PyPI**:
   ```bash
   python -m twine upload dist/*
   ```

## Verification

After publishing, verify the package:

1. **Check PyPI**: https://pypi.org/project/pyprotect/
2. **Test installation**:
   ```bash
   pip install pyprotect
   pyprotect --help
   ```

## Updating the Package

To publish a new version:

1. **Update version** in `pyproject.toml`:
   ```toml
   version = "1.0.1"
   ```

2. **Update version** in `setup.py`:
   ```python
   version="1.0.1",
   ```

3. **Update version** in `src/pyprotect/__init__.py`:
   ```python
   __version__ = "1.0.1"
   ```

4. **Follow publishing steps** above

## Security Notes

⚠️ **IMPORTANT SECURITY REMINDERS**:

1. **Never commit `.pypirc`** - It contains your API token
2. **Add to `.gitignore`**:
   ```
   .pypirc
   *.egg-info/
   dist/
   build/
   ```
3. **Rotate tokens** if accidentally exposed
4. **Use TestPyPI** for testing before production upload

## Troubleshooting

### "File already exists"
- Version already published. Increment version number.

### "Invalid credentials"
- Check your `.pypirc` file
- Verify token is valid at https://pypi.org/manage/account/token/

### "Package not found after upload"
- Wait a few minutes for PyPI to index
- Check https://pypi.org/project/pyprotect/

### "Build failed"
- Ensure all required files are present
- Check `MANIFEST.in` includes necessary files
- Verify `pyproject.toml` syntax

## Resources

- [PyPI Documentation](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [Python Packaging Guide](https://packaging.python.org/)

---

**Ready to publish?** Run `./publish.sh` (Linux/macOS) or `.\publish.ps1` (Windows)!

