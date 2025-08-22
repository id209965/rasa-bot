from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.models import User
from app.config import settings


class AuthMiddleware(BaseMiddleware):
    """Middleware to authenticate users and check admin rights"""
    
    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        session: AsyncSession = data.get("session")
        
        if not session:
            return await handler(event, data)
        
        # Get user from database
        result = await session.execute(
            select(User).where(User.telegram_id == event.from_user.id)
        )
        user = result.scalar_one_or_none()
        
        # Add user data to context
        data["user"] = user
        data["is_registered"] = user is not None
        
        # Check if user is admin (by phone number)
        if user:
            data["is_admin"] = user.phone_number in settings.admin_phone_list
        else:
            data["is_admin"] = False
        
        return await handler(event, data)
