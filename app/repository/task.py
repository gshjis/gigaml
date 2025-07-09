# app/repository/task.py
from sqlalchemy import select
from sqlalchemy.sql.expression import false

from app.models import Task
from app.repository.repository import BaseRepository


class TaskRepository(BaseRepository[Task]):
    """Репозиторий для работы с задачами."""

    @property
    def model(self) -> type[Task]:
        """Возвращает модель Task."""
        return Task

    def get_by_category(self, category_id: int) -> list[Task]:
        """Получить активные задачи по категории.

        Args:
            category_id: ID категории для фильтрации

        Returns:
            list[Task]: Список задач или пустой список при ошибке
        """
        try:
            stmt = (
                select(Task)
                .where(Task.category_id == category_id)
                .where(Task.is_deleted.is_(false()))
                .order_by(Task.created_at.desc())
            )
            return list(self.db_session.scalars(stmt).all())
        except Exception:
            return []

    def get_active_tasks(self, limit: int = 100) -> list[Task]:
        """Получить последние активные задачи.

        Args:
            limit: Максимальное количество возвращаемых задач

        Returns:
            list[Task]: Список задач или пустой список при ошибке
        """
        try:
            stmt = (
                select(Task)
                .where(Task.is_deleted.is_(false()))
                .order_by(Task.created_at.desc())
                .limit(limit)
            )
            return list(self.db_session.scalars(stmt).all())
        except Exception:
            return []
