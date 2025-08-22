from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.main import communication_menu_keyboard, back_keyboard
from app.database.models import User

router = Router()


@router.message(F.text == "💬 Общение")
async def communication_menu(
    message: Message,
    session: AsyncSession,
    is_registered: bool,
    state: FSMContext
):
    """Show communication menu"""
    await state.clear()
    
    if not is_registered:
        await message.answer(
            "🔥 Сначала пройдите регистрацию!"
        )
        return
    
    await message.answer(
        "💬 <b>Общение</b>\n\n"
        "Выберите действие:",
        reply_markup=communication_menu_keyboard()
    )


@router.message(F.text == "👥 Друзья")
async def friends_list(
    message: Message,
    session: AsyncSession,
    user: User,
    is_registered: bool
):
    """Show friends list"""
    if not is_registered:
        await message.answer(
            "🔥 Сначала пройдите регистрацию!"
        )
        return
    
    # TODO: Implement friends fetching
    await message.answer(
        "👥 <b>Мои друзья</b>\n\n"
        "📋 У вас пока нет друзей.\n\n"
        "🔍 Попробуйте найти новых друзей!",
        reply_markup=back_keyboard()
    )


@router.message(F.text == "🔍 Поиск друзей")
async def search_friends(
    message: Message,
    session: AsyncSession,
    user: User,
    is_registered: bool
):
    """Search for new friends"""
    if not is_registered:
        await message.answer(
            "🔥 Сначала пройдите регистрацию!"
        )
        return
    
    # TODO: Implement friend search
    await message.answer(
        "🔍 <b>Поиск друзей</b>\n\n"
        "⚠️ Функция в разработке...",
        reply_markup=back_keyboard()
    )
