from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Vacancy:
    id: int
    title: str
    salary: int
    company: str
    description: str
    url: str
    city: str
    date_added: datetime