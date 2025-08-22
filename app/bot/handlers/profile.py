from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.main import main_menu_keyboard
from app.database.models import User

router = Router()


@router.message(F.text == "👤 Мой профиль")
async def my_profile(
    message: Message,
    session: AsyncSession,
    user: User,
    is_registered: bool,
    state: FSMContext
):
    """Show user profile"""
    await state.clear()
    
    if not is_registered:
        await message.answer(
            "🔥 Сначала пройдите регистрацию!"
        )
        return
    
    # Get user interests
    # TODO: Implement user interests fetching
    interests_text = "Не указаны"
    
    profile_text = f"""
👤 <b>Мой профиль</b>

📞 Телефон: {user.phone_number}
👤 Имя: {user.first_name} {user.last_name}
🎂 Возраст: {user.age}
🚪 Пол: {user.gender.value if user.gender else 'Не указан'}
🏡 Регион: TODO
❤️ Интересы: {interests_text}
🗺️ Местоположение: {'Указано' if user.latitude else 'Не указано'}
    """
    
    if user.photo_url:
        await message.answer_photo(
            photo=user.photo_url,
            caption=profile_text
        )
    else:
        await message.answer(profile_text)
        
    # TODO: Add profile editing buttons
