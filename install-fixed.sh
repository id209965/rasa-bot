#!/bin/bash

# Test Bot Installation Script (Fixed version for Rasa compatibility)

set -e

echo "🚀 Test Bot Installation Script (Fixed)"
echo "======================================="

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
echo "1) ⚡ Minimal (RECOMMENDED - fast, stable, modern packages)"
echo "2) 🧠 With Rasa NLP (slower install, may have version conflicts)"
echo "3) 👨‍💻 Development (with testing tools)"
echo "4) 🏭 Production (optimized)"
read -p "Enter your choice (1-4) [default: 1]: " choice
choice=${choice:-1}

case $choice in
    1)
        echo "📦 Installing minimal requirements (RECOMMENDED)..."
        pip install -r requirements-minimal.txt
        echo "✅ Minimal installation complete! Uses modern, stable packages."
        echo "ℹ️  Note: This version doesn't include Rasa NLP but has all other features."
        ;;
    2)
        echo "⚠️  Installing with Rasa (this may take 15-20 minutes)..."
        echo "📦 Installing Rasa and compatible versions..."
        pip install -r requirements.txt
        if [ $? -ne 0 ]; then
            echo "❌ Rasa installation failed due to version conflicts."
            echo "🔄 Falling back to minimal installation..."
            pip install -r requirements-minimal.txt
        else
            echo "✅ Full installation with Rasa complete!"
            echo "ℹ️  Note: You can now use advanced NLP features."
        fi
        ;;
    3)
        echo "📦 Installing development requirements..."
        pip install -r requirements-dev.txt
        echo "✅ Development installation complete!"
        ;;
    4)
        echo "📦 Installing production requirements..."
        pip install -r requirements-prod.txt
        echo "✅ Production installation complete!"
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
    echo ""
    echo "📝 Please edit .env file with your configuration:"
    echo "   - TELEGRAM_BOT_TOKEN=your_bot_token"
    echo "   - API_SECRET_KEY=your_secret_key"
    echo "   - YANDEX_MAPS_API_KEY=your_maps_key (optional)"
    echo "   - ADMIN_PHONES=your_phone_numbers (optional)"
else
    echo "✅ .env file already exists"
fi

# Create data directory
mkdir -p data

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your bot token and other settings"
echo "2. Initialize database: python manage.py init-db"
echo "3. (Optional) Create admin user: python manage.py create-admin"
echo "4. Start the bot: python main.py"
echo ""
echo "🔄 To activate virtual environment in future sessions:"
echo "   source venv/bin/activate"
echo ""
echo "💡 Tips:"
echo "   - For first-time users: choose Minimal installation (option 1)"
echo "   - Rasa NLP adds intelligent conversations but requires more resources"
echo "   - You can always reinstall with different options later"
