from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.main import admin_menu_keyboard, back_keyboard
from app.database.models import User

router = Router()


@router.message(F.text == "⚙️ Админ панель")
async def admin_panel(
    message: Message,
    session: AsyncSession,
    is_registered: bool,
    is_admin: bool,
    state: FSMContext
):
    """Show admin panel"""
    await state.clear()
    
    if not is_registered:
        await message.answer(
            "🔥 Сначала пройдите регистрацию!"
        )
        return
    
    if not is_admin:
        await message.answer(
            "❌ У вас нет прав администратора!"
        )
        return
    
    await message.answer(
        "⚙️ <b>Админ панель</b>\n\n"
        "Выберите действие:",
        reply_markup=admin_menu_keyboard()
    )


@router.message(F.text == "📤 Загрузить данные")
async def upload_data(
    message: Message,
    session: AsyncSession,
    is_admin: bool
):
    """Upload data prompt"""
    if not is_admin:
        await message.answer(
            "❌ У вас нет прав администратора!"
        )
        return
    
    await message.answer(
        "📤 <b>Загрузка данных</b>\n\n"
        "пришлите Excel файл с данными о регионах и интересах.\n\n"
        "📝 Файл должен содержать колонки:\n"
        "• 'regions' - список регионов\n"
        "• 'interests' - список интересов",
        reply_markup=back_keyboard()
    )


@router.message(F.text == "📊 Отчет по пользователям")
async def export_users(
    message: Message,
    session: AsyncSession,
    is_admin: bool
):
    """Export users report"""
    if not is_admin:
        await message.answer(
            "❌ У вас нет прав администратора!"
        )
        return
    
    # TODO: Implement users export
    await message.answer(
        "📊 <b>Отчет по пользователям</b>\n\n"
        "⚠️ Функция в разработке...",
        reply_markup=back_keyboard()
    )


@router.message(F.text == "📈 Отчет по мероприятиям")
async def export_events(
    message: Message,
    session: AsyncSession,
    is_admin: bool
):
    """Export events report"""
    if not is_admin:
        await message.answer(
            "❌ У вас нет прав администратора!"
        )
        return
    
    # TODO: Implement events export
    await message.answer(
        "📈 <b>Отчет по мероприятиям</b>\n\n"
        "⚠️ Функция в разработке...",
        reply_markup=back_keyboard()
    )
