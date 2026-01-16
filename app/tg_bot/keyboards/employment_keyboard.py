from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.tg_bot.config import employments_list


def get_employment_keyboard() -> InlineKeyboardMarkup:
    buttons = []
    employment_types = list(employments_list.keys())

    for emp in employment_types:
        buttons.append([InlineKeyboardButton(text=emp, callback_data=f"employment{employments_list[emp]}")])

    buttons.append([InlineKeyboardButton(text="Не важно", callback_data="emp_any")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)