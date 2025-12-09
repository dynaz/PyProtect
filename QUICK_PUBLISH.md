# Quick Publish Guide

## ✅ Ready to Publish!

Your package is built and ready. Distribution files:
- `pyprotect-1.0.0-py3-none-any.whl` (wheel)
- `pyprotect-1.0.0.tar.gz` (source distribution)

## 🚀 Publish Now

### Option 1: Use the publish script (Recommended)

**Windows (PowerShell):**
```powershell
.\publish.ps1
```

**Linux/macOS:**
```bash
chmod +x publish.sh
./publish.sh
```

### Option 2: Manual publish

```bash
python -m twine upload dist/*
```

## 📦 After Publishing

Once published, users can install with:
```bash
pip install pyprotect
```

And use it:
```bash
pyprotect --help
pyprotect -i file.py -b
```

## 🔗 Links

- **PyPI Package**: https://pypi.org/project/pyprotect/
- **Your Package Page**: Will be available after first upload

## ⚠️ Important Notes

1. **`.pypirc` is in `.gitignore`** - Your token is safe
2. **Version updates**: Change version in `pyproject.toml`, `setup.py`, and `src/pyprotect/__init__.py`
3. **Test first**: Consider testing on TestPyPI before production

## 🎯 Next Steps

1. Run `.\publish.ps1` (or `./publish.sh`)
2. Confirm upload when prompted
3. Wait 2-3 minutes for PyPI to index
4. Test: `pip install pyprotect`
5. Share: `pip install pyprotect` 🎉

---

**Ready?** Run the publish script now!

