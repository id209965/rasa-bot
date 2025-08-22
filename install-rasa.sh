#!/bin/bash

# Script to install Rasa with compatibility fixes
# Try multiple approaches to install Rasa

set -e

echo "🧠 Attempting to install Rasa with compatibility fixes..."
echo "This script will try multiple methods."
echo ""

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Create or activate Rasa environment
if [ ! -d "venv-rasa" ]; then
    echo "📦 Creating separate virtual environment for Rasa..."
    python3 -m venv venv-rasa
else
    echo "✅ Using existing venv-rasa"
fi

echo "🔄 Activating Rasa environment..."
source venv-rasa/bin/activate

echo "📋 Upgrading pip..."
pip install --upgrade pip

# Method 1: Try with downgraded setuptools
echo ""
echo "🔧 Method 1: Installing with compatible setuptools..."
echo "Downgrading setuptools and packaging to compatible versions..."

pip install "setuptools==57.5.0" "packaging==21.3" "wheel<0.37.0"

if pip install rasa==3.6.13 rasa-sdk==3.6.2; then
    echo "✅ Method 1 succeeded! Rasa installed successfully."
    echo ""
    echo "🎉 Rasa installation completed!"
    echo ""
    echo "Next steps:"
    echo "1. Train the model: cd app/rasa && rasa train"
    echo "2. Start Rasa server: rasa run --enable-api --cors '*' --port 5005"
    echo "3. In another terminal, start the main bot: python main.py"
    echo ""
    echo "Or use Docker: docker-compose -f docker-compose-rasa-only.yml up"
    exit 0
fi

echo "⚠️ Method 1 failed. Trying Method 2..."

# Method 2: Try with force reinstall
echo ""
echo "🔧 Method 2: Force reinstall with --no-deps..."

pip install --force-reinstall --no-cache-dir "setuptools==57.5.0" "packaging==21.3"
pip install --no-deps mattermostwrapper==2.2

if pip install --no-cache-dir rasa==3.6.13 rasa-sdk==3.6.2; then
    echo "✅ Method 2 succeeded! Rasa installed successfully."
    exit 0
fi

echo "⚠️ Method 2 failed. Trying Method 3..."

# Method 3: Try with older Python (if available)
echo ""
echo "🔧 Method 3: Checking for Python 3.8 or 3.9..."

if command -v python3.8 &> /dev/null; then
    echo "Found Python 3.8, creating new environment..."
    deactivate || true
    rm -rf venv-rasa-38
    python3.8 -m venv venv-rasa-38
    source venv-rasa-38/bin/activate
    pip install --upgrade pip
    pip install "setuptools==57.5.0" "packaging==21.3"
    
    if pip install rasa==3.6.13 rasa-sdk==3.6.2; then
        echo "✅ Method 3 with Python 3.8 succeeded!"
        echo "Note: Use 'source venv-rasa-38/bin/activate' for Rasa"
        exit 0
    fi
elif command -v python3.9 &> /dev/null; then
    echo "Found Python 3.9, creating new environment..."
    deactivate || true
    rm -rf venv-rasa-39
    python3.9 -m venv venv-rasa-39
    source venv-rasa-39/bin/activate
    pip install --upgrade pip
    pip install "setuptools==57.5.0" "packaging==21.3"
    
    if pip install rasa==3.6.13 rasa-sdk==3.6.2; then
        echo "✅ Method 3 with Python 3.9 succeeded!"
        echo "Note: Use 'source venv-rasa-39/bin/activate' for Rasa"
        exit 0
    fi
else
    echo "Python 3.8 or 3.9 not found, skipping Method 3"
fi

echo ""
echo "❌ All pip installation methods failed."
echo ""
echo "🐳 RECOMMENDED: Use Docker instead"
echo ""
echo "To use Rasa with Docker:"
echo "1. docker-compose -f docker-compose-rasa-only.yml up -d"
echo "2. Wait for training to complete (check logs: docker-compose -f docker-compose-rasa-only.yml logs -f)"
echo "3. Start main bot: python main.py"
echo ""
echo "Alternative: Use the bot without Rasa (all features work except smart dialogs)"
echo "1. pip install -r requirements.txt"
echo "2. python main.py"
echo ""
echo "For more solutions, see: rasa-troubleshooting.md"
