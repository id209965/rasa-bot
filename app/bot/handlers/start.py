from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.main import main_menu_keyboard
from app.bot.states.registration import RegistrationStates
from app.database.models import User

router = Router()


@router.message(CommandStart())
async def start_command(
    message: Message, 
    session: AsyncSession,
    user: User,
    is_registered: bool,
    is_admin: bool,
    state: FSMContext
):
    """Handle /start command"""
    await state.clear()
    
    if is_registered:
        # User is already registered, show main menu
        await message.answer(
            f"Привет, {user.first_name}! 👋\n\n"
            f"Возвращаемся в главное меню:",
            reply_markup=main_menu_keyboard(is_admin)
        )
    else:
        # New user, start registration
        await message.answer(
            "Привет! Добро пожаловать в чат-бот <b>Тест</b>! 🎉\n\n"
            "Для начала работы нам нужно познакомиться.\n\n"
            "📞 <b>Поделитесь своим номером телефона</b> для регистрации:"
        )
        
        # Set registration state
        await state.set_state(RegistrationStates.phone)


@router.message(F.text == "🔙 Назад")
async def back_to_main(
    message: Message,
    user: User,
    is_registered: bool,
    is_admin: bool,
    state: FSMContext
):
    """Back to main menu"""
    await state.clear()
    
    if is_registered:
        await message.answer(
            "🏠 Главное меню:",
            reply_markup=main_menu_keyboard(is_admin)
        )
    else:
        await message.answer(
            "🔥 Сначала пройдите регистрацию!\n\n"
            "📞 Поделитесь своим номером телефона:"
        )
        await state.set_state(RegistrationStates.phone)


@router.message(F.text == "❓ Помощь")
async def help_command(message: Message, is_registered: bool):
    """Show help message"""
    
    if not is_registered:
        await message.answer(
            "🔥 Сначала пройдите регистрацию!"
        )
        return
    
    help_text = """
🤖 <b>Чат-бот Тест - Краткая инструкция</b>

👤 <b>Мой профиль</b>
• Просмотр и редактирование личных данных

💬 <b>Общение</b>
• Список друзей и чаты с ними
• Поиск новых друзей по интересам

🎉 <b>Мероприятия</b>
• Просмотр мероприятий друзей
• Создание собственных мероприятий
• Приглашение друзей
• Просмотр местоположения на карте

🔄 Для возврата в главное меню используйте кнопку "🔙 Назад"
    """
    
    await message.answer(help_text)
