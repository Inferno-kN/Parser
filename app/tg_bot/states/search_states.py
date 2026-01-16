from aiogram.fsm.state import State, StatesGroup


class SearchStates(StatesGroup):
    waiting_keywords = State()
    waiting_city = State()
    waiting_employment = State()
    waiting_salary = State()