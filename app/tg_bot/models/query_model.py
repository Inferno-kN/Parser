from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Query:
    id: int
    user_id: int
    search_params: str
    created_at: datetime