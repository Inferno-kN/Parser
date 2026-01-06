import requests
from app.parsers.config import HH_API_URL


class HHParser:
    def __init__(self):
        self.base_url = HH_API_URL


    def search_vacancies(self, params: dict) -> list:
        api_params = {
            "text": params.get("keywords", "Python"),
            "area": params.get("area", 1),
            "per_page": params.get("per_page", 50)
        }


        if params.get("salary_min"):
            api_params['salary'] = params["salary_min"]
            api_params["only_with_salary"] = True


        if params.get("employment"):
            api_params["employment"] = params["employment"]


        if params.get("experience"):
            api_params["experience"] = params["experience"]


        try:
            response = requests.get(self.base_url, params=api_params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                vacancies = data.get('items', [])
                return vacancies
            else:
                print(f"Ошибка API: {response.status_code}")
                return []
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")
            return []