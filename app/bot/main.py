import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.config import settings
from app.database.connection import init_database, close_database
from app.bot.handlers import start, profile, events, friends, admin
from app.bot.middlewares.auth import AuthMiddleware
from app.bot.middlewares.database import DatabaseMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    """Main bot function"""
    
    # Initialize database
    await init_database()
    logger.info("Database initialized")
    
    # Create bot and dispatcher
    bot = Bot(
        token=settings.telegram_bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Add middlewares
    dp.message.middleware(DatabaseMiddleware())
    dp.callback_query.middleware(DatabaseMiddleware())
    dp.message.middleware(AuthMiddleware())
    dp.callback_query.middleware(AuthMiddleware())
    
    # Include routers
    dp.include_router(start.router)
    dp.include_router(profile.router)
    dp.include_router(events.router)
    dp.include_router(friends.router)
    dp.include_router(admin.router)
    
    try:
        logger.info("Starting bot...")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await close_database()
        logger.info("Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())
