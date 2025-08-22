from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from typing import List, Optional


def main_menu_keyboard(is_admin: bool = False) -> ReplyKeyboardMarkup:
    """Main menu keyboard"""
    builder = ReplyKeyboardBuilder()
    
    # User menu items
    builder.row(
        KeyboardButton(text="👤 Мой профиль"),
        KeyboardButton(text="💬 Общение")
    )
    builder.row(
        KeyboardButton(text="🎉 Мероприятия"),
        KeyboardButton(text="❓ Помощь")
    )
    
    # Admin menu items
    if is_admin:
        builder.row(
            KeyboardButton(text="⚙️ Админ панель")
        )
    
    return builder.as_markup(resize_keyboard=True)


def communication_menu_keyboard() -> ReplyKeyboardMarkup:
    """Communication menu keyboard"""
    builder = ReplyKeyboardBuilder()
    
    builder.row(
        KeyboardButton(text="👥 Друзья"),
        KeyboardButton(text="🔍 Поиск друзей")
    )
    builder.row(
        KeyboardButton(text="🔙 Назад")
    )
    
    return builder.as_markup(resize_keyboard=True)


def events_menu_keyboard() -> ReplyKeyboardMarkup:
    """Events menu keyboard"""
    builder = ReplyKeyboardBuilder()
    
    builder.row(
        KeyboardButton(text="👥 Мероприятия друзей"),
        KeyboardButton(text="📝 Мои мероприятия")
    )
    builder.row(
        KeyboardButton(text="➕ Создать мероприятие")
    )
    builder.row(
        KeyboardButton(text="🔙 Назад")
    )
    
    return builder.as_markup(resize_keyboard=True)


def admin_menu_keyboard() -> ReplyKeyboardMarkup:
    """Admin menu keyboard"""
    builder = ReplyKeyboardBuilder()
    
    builder.row(
        KeyboardButton(text="📤 Загрузить данные"),
        KeyboardButton(text="📊 Отчет по пользователям")
    )
    builder.row(
        KeyboardButton(text="📈 Отчет по мероприятиям")
    )
    builder.row(
        KeyboardButton(text="🔙 Назад")
    )
    
    return builder.as_markup(resize_keyboard=True)


def gender_keyboard() -> InlineKeyboardMarkup:
    """Gender selection keyboard"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(text="👨 Мужской", callback_data="gender:male"),
        InlineKeyboardButton(text="👩 Женский", callback_data="gender:female")
    )
    builder.row(
        InlineKeyboardButton(text="🤷 Не указывать", callback_data="gender:skip")
    )
    
    return builder.as_markup()


def regions_keyboard(regions: List[tuple]) -> InlineKeyboardMarkup:
    """Regions selection keyboard"""
    builder = InlineKeyboardBuilder()
    
    for region_id, region_name in regions:
        builder.row(
            InlineKeyboardButton(
                text=region_name, 
                callback_data=f"region:{region_id}"
            )
        )
    
    return builder.as_markup()


def interests_keyboard(interests: List[tuple], selected: List[int] = None) -> InlineKeyboardMarkup:
    """Interests selection keyboard"""
    if selected is None:
        selected = []
    
    builder = InlineKeyboardBuilder()
    
    for interest_id, interest_name in interests:
        text = f"✅ {interest_name}" if interest_id in selected else interest_name
        builder.row(
            InlineKeyboardButton(
                text=text,
                callback_data=f"interest:{interest_id}"
            )
        )
    
    if selected:
        builder.row(
            InlineKeyboardButton(
                text="✅ Готово",
                callback_data="interests:done"
            )
        )
    
    return builder.as_markup()


def back_keyboard() -> ReplyKeyboardMarkup:
    """Simple back keyboard"""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔙 Назад")]],
        resize_keyboard=True
    )


def skip_keyboard() -> InlineKeyboardMarkup:
    """Skip button keyboard"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⏭️ Пропустить", callback_data="skip")]
        ]
    )


def confirm_keyboard() -> InlineKeyboardMarkup:
    """Confirm/Cancel keyboard"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Да", callback_data="confirm:yes"),
                InlineKeyboardButton(text="❌ Нет", callback_data="confirm:no")
            ]
        ]
    )


def event_actions_keyboard(event_id: int, is_participant: bool = False, is_creator: bool = False) -> InlineKeyboardMarkup:
    """Event actions keyboard"""
    builder = InlineKeyboardBuilder()
    
    if not is_creator:
        if is_participant:
            builder.row(
                InlineKeyboardButton(
                    text="❌ Покинуть мероприятие",
                    callback_data=f"event_leave:{event_id}"
                )
            )
        else:
            builder.row(
                InlineKeyboardButton(
                    text="✅ Участвовать",
                    callback_data=f"event_join:{event_id}"
                )
            )
    
    builder.row(
        InlineKeyboardButton(
            text="🗺️ Показать на карте",
            callback_data=f"event_map:{event_id}"
        )
    )
    
    if is_creator:
        builder.row(
            InlineKeyboardButton(
                text="👥 Участники",
                callback_data=f"event_participants:{event_id}"
            )
        )
    
    return builder.as_markup()
