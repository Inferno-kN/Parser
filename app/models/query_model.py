from sqlalchemy import Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import List, Dict, Any

from models.base_model import Base


class Query(Base):
    __tablename__ = 'queries'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    search_params: Mapped[Dict[str, Any]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    user: Mapped['User'] = relationship("User", back_populates="queries")

    vacancies: Mapped[List['Vacancy']] = relationship(
        "Vacancy",
        secondary="query_vacancy",
        back_populates="queries"
    )