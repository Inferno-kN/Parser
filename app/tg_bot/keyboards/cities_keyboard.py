from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.tg_bot.config import city_list


def get_cities_keyboard() -> InlineKeyboardMarkup:
    buttons = []
    cities = list(city_list.keys())

    for i in range(0, len(cities), 2):
        row = []
        if i < len(cities):
            row.append(InlineKeyboardButton(text=cities[i], callback_data=f"city{cities[i]}"))
        if i + 1 < len(cities):
            row.append(InlineKeyboardButton(text=cities[i + 1], callback_data=f"city{cities[i + 1]}"))
        if row:
            buttons.append(row)

    return InlineKeyboardMarkup(inline_keyboard=buttons)