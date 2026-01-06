from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base_model import Base
from app.models import user_model, vacancy_model, query_model
from app.models import query_vacancy


db_path = "sqlite:///vacancy.db"
engine = create_engine(db_path, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)