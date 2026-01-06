from sqlalchemy import Integer, String, DateTime, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import List

from models.base_model import Base

class Vacancy(Base):
    __tablename__ = 'vacancies'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    salary: Mapped[int] = mapped_column(Integer, nullable=False)
    company: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    url: Mapped[str] = mapped_column(String(255))
    employment: Mapped[str] = mapped_column(String(255))
    experience: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(100))
    date_added: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    queries: Mapped[List['Query']] = relationship(
        "Query",
        secondary="query_vacancy",
        back_populates="vacancies"
    )