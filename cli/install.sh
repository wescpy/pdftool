#!/bin/bash

# PDF Tool CLI - Installation Script

echo "PDF Tool CLI - Installation"
echo "============================"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.6 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Install dependencies
echo "Installing dependencies..."
if pip3 install -r requirements.txt; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Make script executable
chmod +x pdf_tool.py
echo "✅ Made pdf_tool.py executable"

# Test the installation
echo "Testing installation..."
if python3 pdf_tool.py --help &> /dev/null; then
    echo "✅ Installation successful!"
    echo ""
    echo "Usage:"
    echo "  python3 pdf_tool.py                    # Interactive mode"
    echo "  python3 pdf_tool.py --help             # Show help"
    echo "  python3 pdf_tool.py merge file1.pdf file2.pdf"
    echo "  python3 pdf_tool.py delete file.pdf -p \"1,3-5\""
    echo "  python3 pdf_tool.py info file.pdf"
else
    echo "❌ Installation test failed"
    exit 1
fi 