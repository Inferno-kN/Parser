from aiogram import types
from app.parsers.hh_parser import HHParser
from app.parsers.config import HH_API_URL
from app.tg_bot.config import employments_list
from app.database.session import SessionLocal, create_tables
from app.models.vacancy_model import Vacancy
from datetime import datetime

parser = HHParser(HH_API_URL)


async def prepare_search_params(user_data: dict, salary_min: int) -> dict:
    params = {
        "keywords": user_data.get("keywords", ""),
        "area": user_data.get("area", 1),
        "per_page": 15,
    }

    if salary_min:
        params["salary_min"] = salary_min

    if user_data.get("employment"):
        params["employment"] = user_data["employment"]

    params["experience"] = "between1And3"

    return params


async def show_search_params(message: types.Message, user_data: dict, salary_min: int):
    city_name = user_data.get("city", "Москва")
    employment = user_data.get("employment")

    employment_text = "не важно"
    if employment:
        employment_text = next((k for k, v in employments_list.items() if v == employment), employment)

    summary = (
        "🎯Параметры поиска:\n\n"
        f"Ключевые слова: {user_data['keywords']}\n"
        f"Город: {city_name}\n"
        f"Тип занятости: {employment_text}\n"
        f"Зарплата от: {salary_min or 'не важно'} руб\n\n"
        "🔍Начинаю поиск подождите некоторое время...\n"
        "⏱️Это займет 10-20 секунд"
    )

    await message.answer(summary)


async def search_and_display_vacancies(message: types.Message, search_params: dict):
    try:
        await message.answer("⏳Ищу вакансии, подождите немножко...")

        search_params["per_page"] = 20
        vacancies = parser.search_vacancies(search_params)

        if not vacancies:
            await message.answer("😕По вашему запросу ничего не найдено.\nПопробуйте изменить параметры.")
            return

        create_tables()
        session = SessionLocal()

        saved_count = 0
        max_vacancies = 15

        if len(vacancies) > max_vacancies:
            await message.answer(f"✅Найдено {len(vacancies)} вакансий. Показаны первые {max_vacancies}:")
            vacancies_to_show = vacancies[:max_vacancies]
        else:
            await message.answer(f"✅Найдено {len(vacancies)} вакансий:")
            vacancies_to_show = vacancies


        for i, vac in enumerate(vacancies_to_show, 1):
            vacancy_text = format_vacancy_message(vac, i)
            if vacancy_text:
                await message.answer(vacancy_text, disable_web_page_preview=True)


            try: #пробуем сохранять в модель вакансии
                vacancy_model = create_vacancy_model_from_api(vac)
                if vacancy_model:
                    session.add(vacancy_model)
                    saved_count += 1
            except Exception as e:
                print(f"Ошибка при сохранении вакансии: {e}")


        try: # сохраняем и закрываем бд
            session.commit()
            if saved_count > 0:
                await message.answer(f"💾Сохранено в базу данных: {saved_count} вакансий")
        except Exception as e:
            session.rollback()
            await message.answer(f"⚠️Не удалось сохранить в БД: {str(e)}")

        session.close()


    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}")


def format_vacancy_message(vacancy_data: dict, index: int) -> str:
    if not vacancy_data:
        return ""

    try:
        title = vacancy_data.get('name', 'Без названия')
        salary = vacancy_data.get('salary', {}) or {}
        employer = vacancy_data.get('employer', {}) or {}
        company = employer.get('name', 'Неизвестно')
        url = vacancy_data.get('alternate_url', '')
        area = vacancy_data.get('area', {}) or {}
        city = area.get('name', 'Не указан')

        text = f"{index}. {title}\n"
        text += f"🏢Компания: {company}\n"
        text += f"📍Город: {city}\n"

        salary_from = salary.get('from')
        salary_to = salary.get('to')
        currency = salary.get('currency', 'руб')

        if salary_from or salary_to:
            salary_text = f"{salary_from or '?'}-{salary_to or '?'} {currency}"
            text += f"💰Зарплата: {salary_text}\n"

        if url:
            text += f"🔗[Смотреть вакансию]({url})"
        return text

    except Exception as e:
        print(f"Ошибка форматирования вакансии: {e}")
        return ""


def create_vacancy_model_from_api(vacancy_data: dict):
    try:
        title = vacancy_data.get('name', 'Без названия')

        salary_data = vacancy_data.get('salary', {}) or {}
        salary_from = salary_data.get('from')
        salary_str = str(salary_from) if salary_from else "зарплата не указана"

        employer_data = vacancy_data.get('employer', {}) or {}
        company = employer_data.get('name', 'Неизвестно')

        area_data = vacancy_data.get('area', {}) or {}
        city = area_data.get('name', 'Не указан')

        employment_data = vacancy_data.get('employment', {}) or {}
        employment = employment_data.get('name', '')

        experience_data = vacancy_data.get('experience', {}) or {}
        experience = experience_data.get('name', '')

        url = vacancy_data.get('alternate_url', '')

        description = "Нет описания"

        return Vacancy(
            title=title,
            salary=salary_str,
            company=company,
            description=description,
            url=url,
            employment=employment,
            experience=experience,
            city=city,
            date_added=datetime.now()
        )

    except Exception as e:
        print(f"Ошибка создания модели вакансии: {e}")
        return None