from abc import ABC, abstractmethod
from typing import Generic, Optional, Sequence, TypeVar
from app.models.base import Base

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T", bound=Base)

class BaseRepository(ABC, Generic[T]):
    """Базовый репозиторий для CRUD-операций с поддержкой Soft Delete."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    @property
    @abstractmethod
    def model(self) -> type[T]:
        """Абстрактное свойство для получения модели данных."""
        raise NotImplementedError

    async def get(self, id: int, include_deleted: bool = False) -> Optional[T]:
        """Получить объект по ID.

        Args:
            id: ID объекта
            include_deleted: Если True, вернет даже мягко удаленные объекты

        Returns:
            Объект или None если не найден
        """
        query = select(self.model).where(self.model.id == id)

        if not include_deleted and hasattr(self.model, "is_deleted"):
            query = query.where(self.model.is_deleted.is_(False))

        result = await self.db_session.scalar(query)
        return result

    async def get_all(self, include_deleted: bool = False) -> Sequence[T]:
        """Получить все объекты.

        Args:
            include_deleted: Если True, вернет даже удаленные объекты

        Returns:
            Список объектов
        """
        query = select(self.model).order_by(self.model.created_at.desc())

        if not include_deleted and hasattr(self.model, "is_deleted"):
            query = query.where(self.model.is_deleted.is_(False))

        result = await self.db_session.scalars(query)
        return result.all()

    async def create(self, data: T) -> T:
        """Создать новый объект.

        Args:
            data: Объект для создания

        Returns:
            Созданный объект
        """
        self.db_session.add(data)
        await self.db_session.commit()
        await self.db_session.refresh(data)
        return data

    async def delete(self, id: int, hard_delete: bool = False) -> bool:
        """Удалить объект.

        Args:
            id: ID объекта
            hard_delete: Если True, выполнит физическое удаление

        Returns:
            True если удаление успешно, False если объект не найден
        """
        obj = await self.get(id, include_deleted=True)
        if not obj:
            return False

        if hard_delete or not hasattr(obj, "is_deleted"):
            await self.db_session.delete(obj)
        else:
            obj.is_deleted = True

        await self.db_session.commit()
        return True

    async def restore(self, id: int) -> bool:
        """Восстановить мягко удаленный объект.

        Args:
            id: ID объекта для восстановления

        Returns:
            True если восстановление успешно, False если объект не найден
            или не был удален
        """
        if not hasattr(self.model, "is_deleted"):
            return False

        obj = await self.get(id, include_deleted=True)
        if not obj or not obj.is_deleted:
            return False

        obj.is_deleted = False
        await self.db_session.commit()
        return True

    async def update(self, obj: T) -> T:
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

        await self.db_session.commit()
        await self.db_session.refresh(obj)
        return obj
