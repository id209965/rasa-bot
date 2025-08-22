@echo off

echo 🚀 Test Bot Installation Script (Windows)
echo =======================================

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is required but not installed.
    echo Please download and install Python from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found

:: Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

echo 📋 Upgrading pip...
pip install --upgrade pip

echo.
echo Choose installation type:
echo 1) Full installation (with Rasa NLP)
echo 2) Minimal installation (without Rasa)
echo 3) Development installation
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo 📦 Installing full requirements...
    pip install -r requirements.txt
) else if "%choice%"=="2" (
    echo 📦 Installing minimal requirements...
    pip install -r requirements-minimal.txt
) else if "%choice%"=="3" (
    echo 📦 Installing development requirements...
    pip install -r requirements-dev.txt
) else (
    echo ❌ Invalid choice. Installing minimal requirements...
    pip install -r requirements-minimal.txt
)

:: Setup environment file
if not exist ".env" (
    echo ⚙️ Creating .env file...
    copy .env.example .env
    echo.
    echo 📝 Please edit .env file with your configuration:
    echo    - TELEGRAM_BOT_TOKEN=your_bot_token
    echo    - API_SECRET_KEY=your_secret_key
    echo    - YANDEX_MAPS_API_KEY=your_maps_key
    echo    - ADMIN_PHONES=your_phone_numbers
) else (
    echo ✅ .env file already exists
)

:: Create data directory
if not exist "data" mkdir data

echo.
echo 🎉 Installation completed!
echo.
echo Next steps:
echo 1. Edit .env file with your configuration
echo 2. Initialize database: python manage.py init-db
echo 3. Start the bot: python main.py
echo.
echo To activate virtual environment in future sessions:
echo    venv\Scripts\activate.bat

pause
