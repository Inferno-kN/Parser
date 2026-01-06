from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user_model import User

def create_user(session: Session, name: str, telegram_id: str, email: str = None) -> User:
    user = User(name=name, telegram_id=str(telegram_id), email=email)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user_by_name(session: Session, name: str) -> User:
    statement = select(User).where(User.name == name)
    return session.scalars(statement).first()

def get_user_by_telegram_id(session: Session, telegram_id: str) -> User:
    statement = select(User).where(User.telegram_id == telegram_id)
    return session.scalars(statement).first()