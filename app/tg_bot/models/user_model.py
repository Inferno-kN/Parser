from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class User:
    id: int
    name: str
    telegram_id: int
    email: str
    created_at: datetime