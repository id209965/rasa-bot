from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.main import events_menu_keyboard, back_keyboard
from app.database.models import User

router = Router()


@router.message(F.text == "🎉 Мероприятия")
async def events_menu(
    message: Message,
    session: AsyncSession,
    is_registered: bool,
    state: FSMContext
):
    """Show events menu"""
    await state.clear()
    
    if not is_registered:
        await message.answer(
            "🔥 Сначала пройдите регистрацию!"
        )
        return
    
    await message.answer(
        "🎉 <b>Мероприятия</b>\n\n"
        "Выберите действие:",
        reply_markup=events_menu_keyboard()
    )


@router.message(F.text == "👥 Мероприятия друзей")
async def friends_events(
    message: Message,
    session: AsyncSession,
    user: User,
    is_registered: bool
):
    """Show friends' events"""
    if not is_registered:
        await message.answer(
            "🔥 Сначала пройдите регистрацию!"
        )
        return
    
    # TODO: Implement friends events fetching
    await message.answer(
        "👥 <b>Мероприятия друзей</b>\n\n"
        "📋 Пока нет мероприятий от друзей.\n\n"
        "👥 Найдите друзей через меню 'Общение'!",
        reply_markup=back_keyboard()
    )


@router.message(F.text == "📝 Мои мероприятия")
async def my_events(
    message: Message,
    session: AsyncSession,
    user: User,
    is_registered: bool
):
    """Show user's events"""
    if not is_registered:
        await message.answer(
            "🔥 Сначала пройдите регистрацию!"
        )
        return
    
    # TODO: Implement user events fetching
    await message.answer(
        "📝 <b>Мои мероприятия</b>\n\n"
        "📋 У вас пока нет мероприятий.\n\n"
        "➕ Создайте первое мероприятие!",
        reply_markup=back_keyboard()
    )


@router.message(F.text == "➕ Создать мероприятие")
async def create_event(
    message: Message,
    session: AsyncSession,
    user: User,
    is_registered: bool
):
    """Start event creation"""
    if not is_registered:
        await message.answer(
            "🔥 Сначала пройдите регистрацию!"
        )
        return
    
    # TODO: Implement event creation
    await message.answer(
        "➕ <b>Создание мероприятия</b>\n\n"
        "⚠️ Функция в разработке...",
        reply_markup=back_keyboard()
    )
