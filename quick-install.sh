#!/bin/bash

# Quick Install Script for Test Bot
# This script installs the bot without Rasa for maximum compatibility

set -e

echo "🚀 Quick Install for Test Bot"
echo "============================="
echo "This will install the bot WITHOUT Rasa for maximum compatibility."
echo "You can add Rasa later if needed."
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8+ from https://python.org"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create and activate virtual environment
if [ -d "venv" ]; then
    echo "📦 Using existing virtual environment..."
else
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install working requirements
echo "📦 Installing dependencies (this may take a few minutes)..."
pip install -r requirements-working.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
else
    echo "❌ Installation failed. Trying minimal approach..."
    pip install fastapi==0.104.1 aiogram==3.2.0 sqlalchemy==2.0.23 aiosqlite==0.19.0 uvicorn[standard]==0.24.0
fi

# Setup .env file
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env configuration file..."
    cp .env.example .env
    echo "📝 Please edit the .env file with your bot token:"
    echo "   nano .env"
    echo "   # Set TELEGRAM_BOT_TOKEN=your_bot_token_here"
else
    echo "✅ .env file already exists"
fi

# Create data directory
mkdir -p data

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file: nano .env"
echo "2. Add your bot token: TELEGRAM_BOT_TOKEN=your_token_here"
echo "3. Initialize database: python manage.py init-db"
echo "4. Start the bot: python main.py"
echo ""
echo "💡 To activate this environment later:"
echo "   source venv/bin/activate"
echo ""
echo "ℹ️  This installation does NOT include Rasa NLP."
echo "   The bot will work fully but without advanced conversation features."
echo "   You can add Rasa later if needed."
