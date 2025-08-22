#!/bin/bash

# Test Bot Installation Script

set -e

echo "🚀 Test Bot Installation Script"
echo "=============================="

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Found Python $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "🔄 Activating virtual environment..."
source venv/bin/activate

echo "📋 Upgrading pip..."
pip install --upgrade pip

# Ask user what to install
echo ""
echo "Choose installation type:"
echo "1) Full installation (with Rasa NLP)"
echo "2) Minimal installation (without Rasa)"
echo "3) Development installation"
read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo "📦 Installing full requirements..."
        pip install -r requirements.txt
        ;;
    2)
        echo "📦 Installing minimal requirements..."
        pip install -r requirements-minimal.txt
        ;;
    3)
        echo "📦 Installing development requirements..."
        pip install -r requirements-dev.txt
        ;;
    *)
        echo "❌ Invalid choice. Installing minimal requirements..."
        pip install -r requirements-minimal.txt
        ;;
esac

# Setup environment file
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file..."
    cp .env.example .env
    echo "📝 Please edit .env file with your configuration:"
    echo "   - TELEGRAM_BOT_TOKEN=your_bot_token"
    echo "   - API_SECRET_KEY=your_secret_key"
    echo "   - YANDEX_MAPS_API_KEY=your_maps_key"
    echo "   - ADMIN_PHONES=your_phone_numbers"
else
    echo "✅ .env file already exists"
fi

# Create data directory
mkdir -p data

echo ""
echo "🎉 Installation completed!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Initialize database: python manage.py init-db"
echo "3. Start the bot: python main.py"
echo ""
echo "To activate virtual environment in future sessions:"
echo "   source venv/bin/activate"
