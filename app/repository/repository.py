from abc import ABC, abstractmethod
from typing import Generic, Optional, Sequence, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """Базовый репозиторий для CRUD-операций с поддержкой Soft Delete."""

    def __init__(self, db_session: Session):
        self.db_session = db_session

    @property
    @abstractmethod
    def model(self) -> type[T]:
        """Абстрактное свойство для получения модели данных."""
        raise NotImplementedError

    def get(self, id: int, include_deleted: bool = False) -> Optional[T]:
        """Получить объект по ID.

        Args:
            id: ID объекта
            include_deleted: Если True, вернет даже удаленные объекты

        Returns:
            Объект или None если не найден
        """
        query = select(self.model).where(self.model.id == id)

        if not include_deleted and hasattr(self.model, "is_deleted"):
            query = query.where(self.model.is_deleted.is_(False))

        return self.db_session.scalar(query)

    def get_all(self, include_deleted: bool = False) -> Sequence[T]:
        """Получить все объекты.

        Args:
            include_deleted: Если True, вернет даже удаленные объекты

        Returns:
            Список объектов
        """
        query = select(self.model).order_by(self.model.created_at.desc())

        if not include_deleted and hasattr(self.model, "is_deleted"):
            query = query.where(self.model.is_deleted.is_(False))

        return self.db_session.scalars(query).all()

    def create(self, data: T) -> T:
        """Создать новый объект.

        Args:
            data: Объект для создания

        Returns:
            Созданный объект
        """
        self.db_session.add(data)
        self.db_session.commit()
        self.db_session.refresh(data)
        return data

    def delete(self, id: int, hard_delete: bool = False) -> bool:
        """Удалить объект.

        Args:
            id: ID объекта
            hard_delete: Если True, выполнит физическое удаление

        Returns:
            True если удаление успешно, False если объект не найден
        """
        obj = self.get(id, include_deleted=True)
        if not obj:
            return False

        if hard_delete or not hasattr(obj, "is_deleted"):
            self.db_session.delete(obj)
        else:
            obj.is_deleted = True

        self.db_session.commit()
        return True

    def restore(self, id: int) -> bool:
        """Восстановить мягко удаленный объект.

        Args:
            id: ID объекта для восстановления

        Returns:
            True если восстановление успешно, False если объект не найден
            или не был удален
        """
        if not hasattr(self.model, "is_deleted"):
            return False

        obj = self.get(id, include_deleted=True)
        if not obj or not obj.is_deleted:
            return False

        obj.is_deleted = False
        self.db_session.commit()
        return True
    
    def update(self, obj: T) -> T:
        """Обновить существующий объект модели.

        Args:
            obj: Объект модели с обновленными данными

        Returns:
            Обновленный объект модели

        Raises:
            ValueError: Если объект не привязан к сессии
        """
        if obj not in self.db_session:
            raise ValueError("Object is not attached to the current session")
        
        self.db_session.commit()
        self.db_session.refresh(obj)
        return obj

