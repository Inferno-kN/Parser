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
    city_input = input("Введите город (1-Москва, 2-СПб) >> ")
    salary_input = input("Минимальная зарплата (оставьте пустым если не важно) >> ")

    area = int(city_input) if city_input.isdigit() else 1
    salary_min = int(salary_input) if salary_input.isdigit() else None

    search_params = {
        "keywords": keywords,
        "salary_min": salary_min,
        "area": area,
        "employment": "full",
        "experience": "between1And3",
        "per_page": 10
    }

    raw_vacancies = parser.search_vacancies(search_params)

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