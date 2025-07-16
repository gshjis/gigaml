# app/repository/task.py
from sqlalchemy import select
from sqlalchemy.sql.expression import false
import logging

from app.models import Task
from app.repository.repository import BaseRepository

logger = logging.getLogger(__name__)

class TaskRepository(BaseRepository[Task]):
    """Репозиторий для работы с задачами."""

    @property
    def model(self) -> type[Task]:
        """Возвращает модель Task."""
        return Task

    async def get_by_category(self, category_id: int) -> list[Task]:
        """Получить активные задачи по категории.

        Args:
            category_id: ID категории для фильтрации

        Returns:
            list[Task]: Список задач или пустой список при ошибке
        """
        try:
            logger.info("Fetching active tasks for category ID: %s", category_id)
            stmt = (
                select(Task)
                .where(Task.category_id == category_id)
                .where(Task.is_deleted.is_(false()))
                .order_by(Task.created_at.desc())
            )
            tasks = list((await self.db_session.scalars(stmt)).all())
            logger.info("Fetched %s tasks for category ID: %s", len(tasks), category_id)
            return tasks
        except Exception as e:
            logger.error("Failed to fetch tasks for category ID: %s. Error: %s", category_id, e)
            return []

    async def get_tasks_by_user_id(self, user_id: int, include_deleted: bool = False) -> list[Task]:
        """Получить задачи пользователя по user_id с учетом флага soft delete.

        Args:
            user_id: ID пользователя
            include_deleted: Флаг для включения удаленных задач (по умолчанию False)

        Returns:
            list[Task]: Список задач или пустой список при ошибке
        """
        try:
            logger.info("Fetching tasks for user ID: %s with include_deleted: %s", user_id, include_deleted)
            stmt = (
                select(Task)
                .where(Task.owner_id == user_id)
                .where(Task.is_deleted.is_(include_deleted))
                .order_by(Task.created_at.desc())
            )
            tasks = list((await self.db_session.scalars(stmt)).all())
            logger.info("Fetched %s tasks for user ID: %s", len(tasks), user_id)
            return tasks
        except Exception as e:
            logger.error("Failed to fetch tasks for user ID: %s. Error: %s", user_id, e)
            return []
        