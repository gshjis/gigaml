from abc import ABC, abstractmethod
from typing import Generic, Optional, Sequence, TypeVar

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db_session

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """Базовый репозиторий для CRUD-операций."""

    def __init__(self, db_session: Session = Depends(get_db_session)):
        self.db_session = db_session

    @property
    @abstractmethod
    def model(self) -> type[T]:
        raise NotImplementedError

    def get(self, id: int) -> Optional[T]:
        """Получить объект по ID."""
        return self.db_session.get(self.model, id)

    def get_all(self) -> Sequence[T]:
        """Получить все объекты."""
        stmt = select(self.model).order_by(self.model.created_at.desc())
        return self.db_session.scalars(stmt).all()

    def create(self, data: T) -> T:
        """Создать новый объект."""
        self.db_session.add(data)
        self.db_session.commit()
        self.db_session.refresh(data)
        return data

    def delete(self, id: int) -> bool:
        """Удалить объект."""
        obj = self.get(id)
        if not obj:
            return False
        self.db_session.delete(obj)
        self.db_session.commit()
        return True
