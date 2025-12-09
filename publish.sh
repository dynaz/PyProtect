#!/bin/bash
# PyProtect PyPI Publishing Script

set -e  # Exit on error

echo "🚀 Publishing PyProtect to PyPI"
echo "================================"
echo ""

# Check if build tools are installed
echo "📦 Checking build tools..."
if ! command -v python -m build &> /dev/null; then
    echo "Installing build tools..."
    python -m pip install --upgrade build twine
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info
echo "✅ Cleaned"

# Build the package
echo ""
echo "🔨 Building package..."
python -m build
echo "✅ Build complete"

# Check the distribution
echo ""
echo "📋 Built files:"
ls -lh dist/

# Ask for confirmation
echo ""
read -p "📤 Upload to PyPI? (y/N): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Upload cancelled"
    exit 0
fi

# Upload to PyPI
echo ""
echo "📤 Uploading to PyPI..."
python -m twine upload dist/*

echo ""
echo "🎉 Successfully published to PyPI!"
echo ""
echo "📦 Install with: pip install pyprotect"
echo "🔗 View at: https://pypi.org/project/pyprotect/"

