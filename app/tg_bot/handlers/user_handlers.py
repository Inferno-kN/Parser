from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from app.parsers.hh_parser import HHParser
from app.parsers.config import HH_API_URL
from app.tg_bot.states.search_states import SearchStates
from app.tg_bot.keyboards.cities_keyboard import get_cities_keyboard
from app.tg_bot.keyboards.employment_keyboard import get_employment_keyboard
from app.tg_bot.config import city_list, employments_list
from app.tg_bot.handlers.support_function import prepare_search_params, show_search_params, search_and_display_vacancies


router = Router()
parser = HHParser(HH_API_URL)
search_states = SearchStates()


@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.reply(
        "👋Привет! Я бот для поиска вакансий с HH.ru\n\n"
        "🔍Используй /search для начала поиска\n"
        "📋/help - помощь по командам"
    )


@router.message(Command("help"))
async def help_handler(message: types.Message):
    help_text = (
        "📋Помощь по командам\n\n"
        "/start - Начало работы\n"
        "/help - Эта справка\n"
        "/search - Поиск вакансий\n\n"
    )
    await message.reply(help_text)


@router.message(Command("search"))
async def start_search(message: types.Message, state: FSMContext):
    await message.reply(
        "🔍Поиск вакансий\n\n"
        "📝Введите ключевые слова(название вакансии) для поиска:\n"
        "Например: Python разработчик, менеджер, бухгалтер"
    )
    await state.set_state(search_states.waiting_keywords)


@router.message(search_states.waiting_keywords)
async def process_keywords(message: types.Message, state: FSMContext):
    if len(message.text) < 5:
        await message.answer("❌Слишком короткий запрос. Введите минимум 5 символов.")
        return

    await state.update_data(keywords=message.text.strip())

    await message.answer(
        "🏙️Выберите город:",
        reply_markup=get_cities_keyboard()
    )
    await state.set_state(search_states.waiting_city)


@router.callback_query(F.data.startswith("city"))
async def process_city(callback: types.CallbackQuery, state: FSMContext):
    city_name = callback.data.replace("city", "")
    area_id = city_list.get(city_name)

    if area_id:
        await state.update_data(city=city_name, area=area_id)

        await callback.message.edit_text(
            f"✅Выбран город: {city_name}\n\n"
            "💼Выберите тип занятости:",
            reply_markup=get_employment_keyboard()
        )
        await callback.answer()
        await state.set_state(search_states.waiting_employment)
    else:
        await callback.answer("❌Такого города нету в моём списке :(")


@router.callback_query(F.data.startswith("employment"))
async def process_employment(callback: types.CallbackQuery, state: FSMContext):
    emp_data = callback.data.replace("employment", "")

    if emp_data == "any":
        employment = None
        emp_text = "не важно"
    else:
        employment = emp_data
        emp_text = next((k for k, v in employments_list.items() if v == employment), employment)

    await state.update_data(employment=employment)

    await callback.message.edit_text(
        f"✅Тип занятости: {emp_text}\n\n"
        "💰Введите минимальную зарплату:\n"
        "Например: 100000\n"
        "Или напишите 'не важно'"
    )
    await callback.answer()
    await state.set_state(search_states.waiting_salary)


@router.message(search_states.waiting_salary)
async def process_salary(message: types.Message, state: FSMContext):
    salary_input = message.text.lower()

    salary_min = None
    if salary_input not in ['не важно', 'любая', '']:
        try:
            salary_min = int(salary_input)
            if salary_min < 0:
                raise ValueError
        except ValueError:
            await message.answer("❌Введите положительное число или 'не важно'")
            return

    user_data = await state.get_data()
    search_params = await prepare_search_params(user_data, salary_min)

    await show_search_params(message, user_data, salary_min)
    await search_and_display_vacancies(message, search_params)
    await state.clear()