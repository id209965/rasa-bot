from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import AsyncSessionLocal


class DatabaseMiddleware(BaseMiddleware):
    """Middleware to provide database session"""
    
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        async with AsyncSessionLocal() as session:
            data["session"] = session
            try:
                return await handler(event, data)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()
