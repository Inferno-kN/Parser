from database.session import SessionLocal, create_tables
from models.vacancy_model import Vacancy
from models.user_model import User
from parsers.hh_parser import HHParser
from datetime import datetime


def simple_test():
    create_tables()
    session = SessionLocal()
    parser = HHParser()

    search_params = {
        "keywords": "Python разработчик",
        "salary_min": 150000,
        "area": 1,
        "employment": "full",
        "experience": "between1And3",
        "per_page": 5
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

        print(f"✅ Вакансия создана:")
        print(f"   Название: {vacancy.title}")
        print(f"   Зарплата: {vacancy.salary}")
        print(f"   Компания: {vacancy.company}")
        print(f"   Занятость: {vacancy.employment}")
        print(f"   Опыт работы: {vacancy.experience}")
        print(f"   Город: {vacancy.city}")


    session.close()


if __name__ == "__main__":
    simple_test()