# PyProtect - Advanced Python Code Obfuscator

![PyProtect Logo](https://img.shields.io/badge/PyProtect-Advanced%20Obfuscation-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.6+-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

PyProtect is a comprehensive Python code obfuscation tool with machine ID binding, designed to protect your Python applications from reverse engineering and unauthorized distribution.

## 🚀 Features

### Core Obfuscation
- **Variable Name Obfuscation**: Transforms readable variable names into obfuscated identifiers
- **String Encryption**: Encrypts string literals using base64 encoding
- **AST Transformation**: Advanced Abstract Syntax Tree manipulation
- **Import Protection**: Secures import statements and module loading

### Machine Binding & Licensing
- **Hardware Fingerprinting**: Generates unique machine identifiers based on CPU, MAC address, and disk serial
- **License Key Generation**: Creates signed license keys with expiration dates
- **Runtime Verification**: Validates licenses on every code execution
- **Tamper Detection**: Detects attempts to modify or bypass protection

### Project Protection
- **Directory Processing**: Obfuscates entire Python projects recursively
- **Package Structure Preservation**: Maintains original project structure
- **Unified Licensing**: Single license file for entire projects
- **Cross-Platform**: Works on Linux, Windows, and macOS

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Command Line Options](#command-line-options)
- [Examples](#examples)
- [Security Features](#security-features)
- [Architecture](#architecture)
- [Limitations](#limitations)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🛠️ Installation

### Prerequisites
- Python 3.6 or higher
- pip package manager

### Install Dependencies
```bash
# No external dependencies required for basic functionality
# For enhanced features, you may need:
pip install pathlib2  # For Python < 3.4 (rarely needed)
```

### Download PyProtect
```bash
# Clone or download the PyProtect files
git clone https://github.com/your-repo/pyprotect.git
cd pyprotect
```

## 🚀 Quick Start

### Protect a Single File
```bash
python3 pyprotect.py my_script.py protected_script.py --bind-machine
```

### Protect an Entire Project
```bash
python3 pyprotect.py -i my_project/ -o protected_project/ --bind-machine --expiration 365
```

### Test Protection
```bash
python3 -c "import protected_script"
# Should work on licensed machine, fail on others
```

## 📖 Usage

### Basic Syntax
```bash
python3 pyprotect.py -i INPUT [-o OUTPUT] [OPTIONS]
```

### Input Types
- **Single File**: `script.py`
- **Directory**: `myproject/` (processes all `.py` files recursively)

### Output Types
- **Single File**: `protected.py` (default: `/dist/filename.py`)
- **Directory**: `protected/` (default: `/dist/inputname/`, maintains input structure)

## ⚙️ Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--bind-machine` | Bind code to current machine hardware | Disabled |
| `--expiration DAYS` | License expiration in days | 365 |
| `--help` | Show help message | - |

## 💡 Examples

### Example 1: Basic File Protection
```bash
# Protect a single Python file (output to /dist/filename.py)
python3 pyprotect.py -i sensitive_code.py

# Or specify custom output
python3 pyprotect.py -i sensitive_code.py -o protected.py
```

### Example 2: Machine-Bound Protection
```bash
# Protect and bind to current machine for 1 year
python3 pyprotect.py -i app.py -o app_protected.py --bind-machine --expiration 365
```

### Example 3: Project Protection
```bash
# Protect entire Django/Flask project (output to dist/)
python3 pyprotect.py -i my_django_project/ --bind-machine

# Or specify custom output directory
python3 pyprotect.py -i my_django_project/ -o protected_project/ --bind-machine
```

### Example 4: Trial Version (30 days)
```bash
# Create time-limited trial version
python3 pyprotect.py -i software.py -o trial_version.py --bind-machine --expiration 30
```

## 🔒 Security Features

### Variable Obfuscation
```python
# Original
def process_data(user_input, api_key="secret123"):
    secret_token = "token_abc123"
    return user_input + secret_token

# Protected
def _obf_0(_obf_1, _obf_2=_decrypt_str('0')):
    _obf_3 = _decrypt_str('1')
    return _obf_1 + _obf_3
```

### String Encryption
```python
# Original strings are base64 encoded
_STRINGS = ['c2VjcmV0MTIz', 'dG9rZW5fYWJjMTIz']  # Encrypted strings
```

### Hardware Binding
- **Machine ID Generation**: Combines CPU, MAC, and disk serial
- **License Validation**: Runtime checks ensure code only runs on authorized machines
- **Expiration Control**: Time-based license expiration

### Runtime Protection
```python
# Automatic license check on import
_check_license()  # Validates machine and expiration
```

## 🏗️ Architecture

### Core Components

1. **AST Processor** (`Obfuscator` class)
   - Parses Python code into Abstract Syntax Tree
   - Transforms variable names and string literals
   - Applies obfuscation rules

2. **License Manager**
   - Generates hardware fingerprints
   - Creates signed license keys
   - Validates licenses at runtime

3. **Runtime Engine**
   - Decrypts strings on-demand
   - Verifies machine authorization
   - Handles tamper detection

### File Structure
```
PyProtect/
├── pyprotect.py          # Main obfuscation tool
├── README.md            # This documentation
├── examples/            # Sample projects
│   ├── basic_script.py
│   └── sample_project/
└── tests/               # Test cases
    ├── test_obfuscation.py
    └── test_licensing.py
```

## ⚠️ Limitations

### Current Limitations
- **F-string Support**: Files containing f-strings may fail (working on fix)
- **Complex Metaclasses**: Advanced Python patterns may need adjustment
- **Dynamic Imports**: `importlib` and dynamic imports may require special handling
- **Third-party Libraries**: Some libraries may not work with obfuscated code

### Known Issues
- Files with f-strings (f"{variable}") may cause parsing errors
- Very large files (>10MB) may be slow to process
- Some debugging tools may not work with obfuscated code

## 🔧 Troubleshooting

### Common Issues

#### "SyntaxError: invalid syntax"
**Cause**: F-strings or advanced Python syntax not supported
**Solution**: Convert f-strings to `.format()` or string concatenation

#### "ModuleNotFoundError"
**Cause**: Import paths changed after obfuscation
**Solution**: Use absolute imports or adjust PYTHONPATH

#### "Unauthorized use of script"
**Cause**: License validation failed
**Solutions**:
- Verify you're on the licensed machine
- Check license hasn't expired
- Regenerate license if hardware changed

#### "ast.Unparse not available"
**Cause**: Python version < 3.9
**Solution**: Upgrade Python or use string fallback mode

### Debug Mode
```bash
# Enable verbose output
python3 pyprotect.py input.py output.py --verbose
```

### Recovery
```bash
# If obfuscation fails, restore from backup
cp original_file.py obfuscated_file.py.backup
```

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. **Fork** the repository
2. **Create** a feature branch
3. **Add** tests for new features
4. **Submit** a pull request

### Development Setup
```bash
git clone https://github.com/dynaz/PyProtect
cd pyprotect
python3 -m pip install -r requirements-dev.txt
python3 -m pytest tests/
```

### Code Standards
- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Include unit tests for new features
- Update documentation for changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Commercial Use
For commercial applications requiring advanced features:
- Enterprise licensing available
- Priority support
- Custom feature development
- Professional services

## 📞 Support

### Documentation
- [API Reference](api.md)
- [Security Guide](security.md)
- [Best Practices](best-practices.md)

### Community
- **GitHub Issues**: Report bugs and request features
- **Discussions**: Ask questions and share experiences
- **Wiki**: Community guides and tutorials

### Professional Support
For enterprise deployments and custom requirements:
- Email: dynaz@mac.com
- Enterprise licensing: dynaz@mac.com

---

## 🎯 Quick Reference

### Most Common Commands
```bash
# Quick protection (output to dist/)
python3 pyprotect.py -i file.py --bind-machine

# Project protection (output to dist/)
python3 pyprotect.py -i project/ --bind-machine

# Trial version (30 days)
python3 pyprotect.py -i app.py -o trial.py --bind-machine --expiration 30
```

### Verification
```bash
# Test protected file
python3 protected.py

# Check license status
python3 -c "from pyprotect import verify_license; print('License valid!')"

# View machine ID
python3 -c "from pyprotect import get_machine_id; print('ID:', get_machine_id())"
```

---

**PyProtect** - Secure your Python code with advanced obfuscation and hardware binding! 🔐✨
