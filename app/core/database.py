# app/core/database.py
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.settings import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session() -> Iterator[Session]:
    """Return DB session"""

    session = SessionLocal()
    try:
        print("Session opened")
        yield session
    finally:
        session.close()
        print("Session closed")
