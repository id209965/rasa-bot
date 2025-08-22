#!/usr/bin/env python3
"""
Management script for Test Bot application.

Usage:
    python manage.py [command] [options]
    
Commands:
    start                    Start the bot and API
    bot                      Start only the bot
    api                      Start only the API
    rasa                     Train and start Rasa server
    init-db                  Initialize database
    create-admin             Create admin user
    test                     Run tests
    """

import sys
import asyncio
import argparse
from pathlib import Path

# Add app directory to path
sys.path.append(str(Path(__file__).parent / "app"))

from app.config import settings
from app.database.connection import init_database, AsyncSessionLocal
from app.database.models import User, Region, Interest
from sqlalchemy import select


async def init_db():
    """Initialize database"""
    print("Initializing database...")
    await init_database()
    
    # Add default regions and interests
    async with AsyncSessionLocal() as session:
        # Check if we already have data
        regions_count = await session.execute(select(Region))
        if not regions_count.scalars().first():
            # Add default regions
            default_regions = [
                "Москва", "СПб", "Новосибирск", "Екатеринбург", 
                "Казань", "Нижний Новгород", "Челябинск", "Самара"
            ]
            for region_name in default_regions:
                region = Region(name=region_name)
                session.add(region)
            
            # Add default interests
            default_interests = [
                "Спорт", "Музыка", "Кино", "Книги", "Программирование",
                "Путешествия", "Кулинария", "Искусство", "Фотография",
                "Игры", "Танцы", "Языки"
            ]
            for interest_name in default_interests:
                interest = Interest(name=interest_name)
                session.add(interest)
            
            await session.commit()
            print(f"Added {len(default_regions)} regions and {len(default_interests)} interests")
    
    print("Database initialized successfully!")


async def create_admin():
    """Create admin user interactively"""
    if not settings.admin_phone_list:
        print("No admin phones configured in settings!")
        print("Please add phone numbers to ADMIN_PHONES environment variable.")
        return
    
    print("Creating admin user...")
    print(f"Available admin phones: {', '.join(settings.admin_phone_list)}")
    
    phone = input("Enter admin phone number: ").strip()
    if phone not in settings.admin_phone_list:
        print(f"Phone {phone} is not in admin list!")
        return
    
    async with AsyncSessionLocal() as session:
        # Check if user already exists
        result = await session.execute(
            select(User).where(User.phone_number == phone)
        )
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            print(f"User with phone {phone} already exists!")
            return
        
        # Get first region
        regions_result = await session.execute(select(Region).limit(1))
        region = regions_result.scalar_one_or_none()
        
        if not region:
            print("No regions found! Please run 'python manage.py init-db' first.")
            return
        
        # Create admin user
        admin_user = User(
            telegram_id=0,  # Will be updated when user starts bot
            phone_number=phone,
            first_name="Admin",
            last_name="User",
            age=30,
            region_id=region.id,
            is_admin=True
        )
        
        session.add(admin_user)
        await session.commit()
        
        print(f"Admin user created successfully with phone {phone}")
        print("User will need to register through the bot to link Telegram account.")


def start_bot():
    """Start only the bot"""
    from app.bot.main import main
    asyncio.run(main())


def start_api():
    """Start only the API"""
    import uvicorn
    from app.api.main import app
    
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        log_level="info" if settings.debug else "warning"
    )


def start_rasa():
    """Start Rasa server"""
    import subprocess
    import os
    
    rasa_dir = Path("app/rasa")
    if not rasa_dir.exists():
        print("Rasa directory not found!")
        return
    
    print("Training Rasa model...")
    os.chdir(rasa_dir)
    
    # Train model
    subprocess.run([
        "rasa", "train", 
        "--domain", "domain.yml",
        "--data", "data/",
        "--config", "config.yml"
    ])
    
    print("Starting Rasa server...")
    # Start server
    subprocess.run([
        "rasa", "run", 
        "--enable-api", 
        "--cors", "*", 
        "--port", "5005"
    ])


def run_tests():
    """Run tests"""
    import subprocess
    
    print("Running tests...")
    result = subprocess.run(["python", "-m", "pytest", "app/tests/", "-v"])
    return result.returncode


def main():
    parser = argparse.ArgumentParser(
        description="Test Bot Management Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        "command",
        choices=["start", "bot", "api", "rasa", "init-db", "create-admin", "test"],
        help="Command to run"
    )
    
    args = parser.parse_args()
    
    if args.command == "start":
        # Start both bot and API
        from main import main as start_all
        start_all()
    
    elif args.command == "bot":
        start_bot()
    
    elif args.command == "api":
        start_api()
    
    elif args.command == "rasa":
        start_rasa()
    
    elif args.command == "init-db":
        asyncio.run(init_db())
    
    elif args.command == "create-admin":
        asyncio.run(create_admin())
    
    elif args.command == "test":
        exit_code = run_tests()
        sys.exit(exit_code)


if __name__ == "__main__":
    main()
