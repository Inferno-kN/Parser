from sqlalchemy import Table, Column, Integer, ForeignKey
from models.base_model import Base


query_vacancy = Table(
    'query_vacancy',
    Base.metadata,
    Column('query_id', Integer, ForeignKey('queries.id'), primary_key=True),
    Column('vacancy_id', Integer, ForeignKey('vacancies.id'), primary_key=True)
)