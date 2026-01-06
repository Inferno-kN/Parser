from aiogram import Router, types
from aiogram.filters.command import Command

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Привет! Я бот для поиска вакансий с HH.ru и LinkedIn. Начни с команды 'search'")


@router.message(Command("help"))
async def help_handler(message: types.Message):
    help_text = ("Помощь по командам\n"
                 "Основные команды:\n"
                 "`start` - Старт работы\n"
                 "`/help` - Это помощь по командам\n"
                 "`/search` - Поиск вакансий\n"
                 "`/profile` - Мой профиль\n"
                 "`/history` - История запросов\n"
                 "`/stats` - Моя статистика\n"
                 )
    await message.answer(help_text)


@router.message(Command("profile"))
async def profile_handler(message: types.Message):
    profile_text = (
            f"Здесь представлен твой профиль\n"
            f"Твой уникальный идентификатор: {message.from_user.id}\n"
            f"Имя: {message.from_user.first_name}\n"
            f"Твой Username: {message.from_user.username or 'не указан'}"
    )
    await message.answer(profile_text)


@router.message(Command("history"))
async def history_handler(message: types.Message):
    await message.reply("История запросов пока пуста")


@router.message(Command("stats"))
async def stats_handler(message: types.Message):
    await message.answer("Статистика: пока нет данных")


@router.message(Command("search"))
async def search_handler(message: types.Message):
    await message.answer(
        "Поиск вакансий\n\n"
        "Функция поиска скоро будет доступна!\n"
        "А пока используй другие команды."
    )