from hh_parser import HHParser


def test_your_parser():
    parser = HHParser()

    # Параметры как в твоём коде (без salary_max)
    search_params = {
        "keywords": "Python разработчик",
        "salary_min": 150000,
        "area": 1,
        "employment": "full",
        "experience": "between1And3",
        "per_page": 5
    }

    print("🧪 ТЕСТ ТВОЕГО ПАРСЕРА (5 параметров)")
    print("=" * 60)
    print("Используются параметры которые РЕАЛЬНО работают:")
    print(f"1. Ключевые слова: '{search_params['keywords']}'")
    print(f"2. Мин. зарплата: {search_params['salary_min']} руб.")
    print(f"3. Город: Москва (area={search_params['area']})")
    print(f"4. Тип занятости: {search_params['employment']} (полная)")
    print(f"5. Опыт: {search_params['experience']} (1-3 года)")
    print("=" * 60)
    print("⚠️ Параметр salary_max ИГНОРИРУЕТСЯ (его нет в коде)")
    print("=" * 60)

    # Вызываем ТВОЙ метод
    vacancies = parser.search_vacancies(search_params)

    print(f"\n📊 РЕЗУЛЬТАТЫ ПОИСКА:")
    print(f"Всего вакансий от API: {len(vacancies)}")

    if not vacancies:
        print("❌ Нет вакансий по заданным критериям")
        return

    print(f"\n🔍 ПЕРВЫЕ {min(3, len(vacancies))} ВАКАНСИИ:")
    print("-" * 50)

    for i, vacancy in enumerate(vacancies[:3], 1):
        print(f"\n{i}. {vacancy.get('name', 'Без названия')}")
        print(f"   🏢 {vacancy.get('employer', {}).get('name', 'Компания не указана')}")
        print(f"   📍 {vacancy.get('area', {}).get('name', 'Город не указан')}")

        # Проверяем зарплату
        salary = vacancy.get('salary')
        if salary:
            salary_from = salary.get('from', '?')
            salary_to = salary.get('to', '?')
            currency = salary.get('currency', 'RUR')
            print(f"   💰 {salary_from} — {salary_to} {currency}")

            if salary_to and salary_to > 300000:
                print(f"   ⚠️  Превышает salary_max=300000 (но в коде нет фильтрации!)")
        else:
            print(f"   💰 Зарплата не указана")

        # Опыт и занятость
        exp = vacancy.get('experience', {}).get('name', 'Не указан')
        emp = vacancy.get('employment', {}).get('name', 'Не указан')
        print(f"   👨‍💻 Опыт: {exp}")
        print(f"   📅 Занятость: {emp}")
        print(f"   🔗 {vacancy.get('alternate_url', 'Нет ссылки')}")

    print(f"\n{'=' * 60}")
    print("📈 СТАТИСТИКА:")

    # Простая статистика
    with_salary = sum(1 for v in vacancies if v.get('salary'))
    print(f"• С зарплатой: {with_salary}/{len(vacancies)}")
    print(f"• Без зарплаты: {len(vacancies) - with_salary}/{len(vacancies)}")

    # Проверка зарплат > 300к
    high_salary = 0
    for v in vacancies:
        salary = v.get('salary')
        if salary and salary.get('to'):
            if salary['to'] > 300000:
                high_salary += 1

    if high_salary > 0:
        print(f"⚠️  Вакансий с зарплатой >300к: {high_salary}")
        print(f"   (параметр salary_max=300000 не применяется!)")

    print(f"{'=' * 60}")
    print("✅ ТЕСТ ЗАВЕРШЕН")
    print("Ваш парсер работает с 5 параметрами (кроме salary_max)")


if __name__ == "__main__":
    test_your_parser()