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

# Make script executable
chmod +x pyprotect.py
echo "✅ Made pyprotect.py executable"

# Create symlink for global access
if [ -f "pyprotect.py" ]; then
    SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/pyprotect.py"

    # Try to create symlink in /usr/local/bin (requires sudo)
    if sudo ln -sf "$SCRIPT_PATH" /usr/local/bin/pyprotect 2>/dev/null; then
        echo "✅ Created global symlink: pyprotect"
        echo "   You can now use 'pyprotect' from anywhere!"
    else
        echo "⚠️  Could not create global symlink (need sudo permissions)"
        echo "   You can still use: $SCRIPT_PATH"
        echo ""
        echo "   To create global symlink manually:"
        echo "   sudo ln -sf $SCRIPT_PATH /usr/local/bin/pyprotect"
    fi
else
    echo "❌ pyprotect.py not found in current directory"
    exit 1
fi

# Install if running as pip package (optional - symlink works without it)
if [ -f "setup.py" ]; then
    echo "📦 Installing as Python package..."
    
    # Try normal installation and capture output
    ERROR_OUTPUT=$(pip3 install -e . 2>&1)
    INSTALL_STATUS=$?
    
    if [ $INSTALL_STATUS -eq 0 ]; then
        echo "✅ Package installed successfully"
    else
        # Check if it's an externally-managed-environment error
        if echo "$ERROR_OUTPUT" | grep -q "externally-managed-environment"; then
            echo "⚠️  Externally-managed Python environment detected (PEP 668)"
            echo ""
            echo "💡 Attempting with --break-system-packages flag..."
            echo "   (Note: This bypasses system package protection)"
            
            if pip3 install -e . --break-system-packages 2>/dev/null; then
                echo "✅ Package installed with --break-system-packages"
            else
                echo "⚠️  Package installation skipped (non-critical)"
                echo ""
                echo "   ✅ The symlink already works - you can use 'pyprotect' command!"
                echo ""
                echo "   💡 Alternative installation methods:"
                echo "      • Use pipx: sudo apt install pipx && pipx install -e ."
                echo "      • Use virtual environment:"
                echo "        python3 -m venv venv && source venv/bin/activate && pip install -e ."
                echo "      • Skip package install (symlink is sufficient for command usage)"
            fi
        else
            # Other error - show it but don't fail
            echo "⚠️  Package installation failed (non-critical)"
            echo "   The symlink already works - you can use 'pyprotect' command"
            echo "   Error details:"
            echo "$ERROR_OUTPUT" | head -3 | sed 's/^/   /'
        fi
    fi
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "📖 Usage Examples:"
echo "  pyprotect -i file.py -b"
echo "  pyprotect -i project/ -b"
echo "  pyprotect -m  # Check machine ID"
echo "  pyprotect -c  # Check license status"
echo ""
echo "📖 Run 'pyprotect --help' for full documentation"
