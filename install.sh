#!/bin/bash
# PyProtect Installation Script

echo "🚀 Installing PyProtect..."
echo "=========================="

# Check Python version
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 is required but not found."
    exit 1
fi

# Install if running as pip package
if [ -f "setup.py" ]; then
    echo "📦 Installing as Python package..."
    pip3 install -e .
else
    echo "✅ PyProtect is ready to use!"
    echo ""
    echo "Usage examples:"
    echo "  python3 pyprotect.py file.py protected.py --bind-machine"
    echo "  python3 pyprotect.py project/ protected/ --bind-machine"
fi

echo ""
echo "🎉 Installation complete!"
echo "📖 Run 'python3 pyprotect.py --help' to get started"
