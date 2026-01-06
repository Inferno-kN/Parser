from database.session import SessionLocal, create_tables
from app.models.vacancy_model import Vacancy
from app.models.user_model import User
from app.parsers.hh_parser import HHParser
from datetime import datetime


def simple_test():
    create_tables()
    session = SessionLocal()
    parser = HHParser()

    keywords = input("Введите ключевые слова >> ")
    city_input = input("""
Выберите город:
1 - Москва
2 - Санкт-Петербург  
3 - Екатеринбург
4 - Новосибирск
5 - Казань
6 - Нижний Новгород
7 - Удаленная работа
8 - Сочи
9 - Красноярск
10 - Челябинск
11 - Волгоград
12 - Ростов-на-Дону
13 - Самара
14 - Омск
15 - Уфа
16 - Пермь
17 - Воронеж
18 - Краснодар
19 - Саратов
20 - Тюмень
21 - Ижевск
22 - Барнаул
23 - Владивосток
24 - Ярославль
Введите номер города >> """)
    salary_input = input("Минимальная зарплата (оставьте пустым если не важно) >> ")

    city_mapping = {
        '1': 1,  # Москва
        '2': 2,  # Санкт-Петербург
        '3': 3,  # Екатеринбург
        '4': 4,  # Новосибирск
        '5': 88,  # Казань
        '6': 66,  # Нижний Новгород
        '7': 113,  # Удаленная работа
        '8': 239,  # Сочи
        '9': 54,  # Красноярск
        '10': 56,  # Челябинск
        '11': 24,  # Волгоград
        '12': 76,  # Ростов-на-Дону
        '13': 78,  # Самара
        '14': 68,  # Омск
        '15': 99,  # Уфа
        '16': 72,  # Пермь
        '17': 26,  # Воронеж
        '18': 53,  # Краснодар
        '19': 70,  # Саратов
        '20': 159,  # Тюмень
        '21': 110,  # Ижевск
        '22': 60,  # Барнаул
        '23': 22,  # Владивосток
        '24': 112  # Ярославль
    }

    area = city_mapping.get(city_input, 1)

    salary_min = int(salary_input) if salary_input.isdigit() else None

    search_params = {
        "keywords": keywords,
        "salary_min": salary_min,
        "area": area,
        "employment": "full",
        "experience": "between1And3",
        "per_page": 10
    }

    print(f"\n🔍 Ищем вакансии в городе с ID: {area}")

    raw_vacancies = parser.search_vacancies(search_params)

    if not raw_vacancies:
        print("❌ Вакансий не найдено")
        return

    for vac in raw_vacancies:
        salary = vac.get('salary')
        salary_from = 0
        if salary is not None:
            salary_from = salary.get('from')
            if salary_from is None:
                salary_from = 0

        vacancy = Vacancy(
            title=vac.get('name', ''),
            salary=str(salary_from),
            company=vac.get('employer', {}).get('name', ''),
            url=vac.get('alternate_url', ''),
            employment=vac.get('employment', {}).get('name', ''),
            experience=vac.get('experience', {}).get('name', ''),
            city=vac.get('area', {}).get('name', ''),
            description=vac.get('snippet', {}).get('responsibility', '') or 'Нет описания',
            date_added=datetime.now()
        )

        session.add(vacancy)
        session.commit()

        print(f"✅ {vacancy.title}")
        print(f"   💰 {vacancy.salary}")
        print(f"   🏢 {vacancy.company}")
        print(f"   📍 {vacancy.city}")

    session.close()


if __name__ == "__main__":
    simple_test()