# app/repository/task.py
import logging

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import false

from app.core.exceptions import DatabaseError, TaskNotFoundException
from app.domain.task import TaskData
from app.models import Task

logger = logging.getLogger(__name__)


class TaskRepository:
    """Репозиторий для работы с задачами."""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create(self, task: TaskData) -> TaskData:
        """Создать новую задачу.

        Args:
            task: Объект задачи для создания

        Returns:
            TaskData: Созданная задача
        """
        try:
            logger.info("Creating task: %s", task)
            db_task = Task(
                name=task.name,
                description=task.description,
                pomodoro_count=task.pomodoro_count,
                category_id=task.category_id,
                owner_id=task.owner_id,
            )
            stmt = insert(Task).values(
                name=db_task.name,
                description=db_task.description,
                pomodoro_count=db_task.pomodoro_count,
                category_id=db_task.category_id,
                owner_id=db_task.owner_id,
            )
            result = await self.db_session.execute(stmt)
            await self.db_session.commit()
            if result.inserted_primary_key:
                task_id = result.inserted_primary_key[0]
                logger.info("Task created successfully with ID: %s", task_id)
                return TaskData(
                    task_id=task_id,
                    name=db_task.name,
                    description=db_task.description,
                    pomodoro_count=db_task.pomodoro_count,
                    category_id=db_task.category_id,
                    owner_id=db_task.owner_id,
                    created_at=task.created_at,
                    updated_at=task.updated_at,
                )
            else:
                logger.error("Failed to create task: No ID generated")
                raise DatabaseError("Failed to create task: No ID generated")
        except Exception as e:
            logger.error("Failed to create task: %s. Error: %s", task, e)
            raise DatabaseError("Failed to create task") from e

    async def get_tasks_by_category(self, category_id: int) -> list[TaskData]:
        """Получить активные задачи по категории.

        Args:
            category_id: ID категории для фильтрации

        Returns:
            list[TaskData]: Список задач или пустой список при ошибке
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
            return [
                TaskData(
                    task_id=task.ID,
                    name=task.name,
                    description=task.description,
                    pomodoro_count=task.pomodoro_count,
                    category_id=task.category_id,
                    owner_id=task.owner_id,
                    created_at=task.created_at,
                    updated_at=task.updated_at,
                )
                for task in tasks
            ]
        except Exception as e:
            logger.error(
                "Failed to fetch tasks for category ID: %s. Error: %s", category_id, e
            )
            return []

    async def get_tasks_by_user_id(
        self, user_id: int, include_deleted: bool = False
    ) -> list[TaskData]:
        """Получить задачи пользователя по user_id с учетом флага soft delete.

        Args:
            user_id: ID пользователя
            include_deleted: Флаг для включения удаленных задач (по умолчанию False)

        Returns:
            list[TaskData]: Список задач или пустой список при ошибке
        """
        try:
            logger.info(
                "Fetching tasks for user ID: %s with include_deleted: %s",
                user_id,
                include_deleted,
            )
            stmt = (
                select(Task)
                .where(Task.owner_id == user_id)
                .where(Task.is_deleted.is_(include_deleted))
                .order_by(Task.created_at.desc())
            )
            tasks = list((await self.db_session.scalars(stmt)).all())
            logger.info("Fetched %s tasks for user ID: %s", len(tasks), user_id)
            return [
                TaskData(
                    task_id=task.ID,
                    name=task.name,
                    description=task.description,
                    pomodoro_count=task.pomodoro_count,
                    category_id=task.category_id,
                    owner_id=task.owner_id,
                    created_at=task.created_at,
                    updated_at=task.updated_at,
                )
                for task in tasks
            ]
        except Exception as e:
            logger.error("Failed to fetch tasks for user ID: %s. Error: %s", user_id, e)
            return []

    async def get_task_by_id(self, task_id: int) -> TaskData | None:
        """Получить задачу по ID.

        Args:
            task_id: ID задачи

        Returns:
            TaskData | None: Задача или None, если задача не найдена
        """
        try:
            logger.info("Fetching task with ID: %s", task_id)
            stmt = select(Task).where(Task.ID == task_id)
            task = (await self.db_session.scalars(stmt)).first()
            if not task:
                logger.debug("Task not found: %s", task_id)
                return None
            logger.info("Task fetched successfully: %s", task_id)
            return TaskData(
                task_id=task.ID,
                name=task.name,
                description=task.description,
                pomodoro_count=task.pomodoro_count,
                category_id=task.category_id,
                owner_id=task.owner_id,
                created_at=task.created_at,
                updated_at=task.updated_at,
            )
        except Exception as e:
            logger.error("Failed to fetch task with ID: %s. Error: %s", task_id, e)
            raise DatabaseError("Failed to fetch task") from e

    async def get_all_tasks(self) -> list[TaskData]:
        """Получить все задачи.

        Returns:
            list[TaskData]: Список всех задач
        """
        try:
            logger.info("Fetching all tasks")
            stmt = select(Task)
            tasks = list((await self.db_session.scalars(stmt)).all())
            logger.info("Fetched %s tasks", len(tasks))
            return [
                TaskData(
                    task_id=task.ID,
                    name=task.name,
                    description=task.description,
                    pomodoro_count=task.pomodoro_count,
                    category_id=task.category_id,
                    owner_id=task.owner_id,
                    created_at=task.created_at,
                    updated_at=task.updated_at,
                )
                for task in tasks
            ]
        except Exception as e:
            logger.error("Failed to fetch all tasks. Error: %s", e)
            raise DatabaseError("Failed to fetch all tasks") from e

    async def delete_task(self, task_id: int, hard_delete: bool = False) -> bool:
        """Удалить задачу по ID.

        Args:
            task_id: ID задачи
            hard_delete: Флаг для выполнения жесткого удаления (по умолчанию False)

        Returns:
            bool: True, если задача успешно удалена, иначе False
        """
        try:
            if hard_delete:
                logger.info("Hard deleting task with ID: %s", task_id)
                delete_stmt = delete(Task).where(Task.ID == task_id)
                result = await self.db_session.execute(delete_stmt)
                await self.db_session.commit()
                if result.rowcount > 0:
                    logger.info("Task hard deleted successfully: %s", task_id)
                    return True
                else:
                    logger.debug("Task not found: %s", task_id)
                    return False
            else:
                logger.info("Soft deleting task with ID: %s", task_id)
                update_stmt = (
                    update(Task).where(Task.ID == task_id).values(is_deleted=True)
                )
                result = await self.db_session.execute(update_stmt)
                await self.db_session.commit()
                if result.rowcount > 0:
                    logger.info("Task soft deleted successfully: %s", task_id)
                    return True
                else:
                    logger.debug("Task not found: %s", task_id)
                    return False
        except Exception as e:
            logger.error("Failed to delete task with ID: %s. Error: %s", task_id, e)
            raise DatabaseError("Failed to delete task") from e

    async def update_task(self, task_id: int, task_data: TaskData) -> TaskData:
        """Обновить задачу по ID.

        Args:
            task_id: ID задачи
            task_data: Данные для обновления задачи

        Returns:
            TaskData: Обновленная задача
        """
        try:
            logger.info("Updating task with ID: %s and data: %s", task_id, task_data)
            stmt = (
                update(Task)
                .where(Task.ID == task_id)
                .values(
                    name=task_data.name,
                    description=task_data.description,
                    pomodoro_count=task_data.pomodoro_count,
                    category_id=task_data.category_id,
                    owner_id=task_data.owner_id,
                )
            )
            result = await self.db_session.execute(stmt)
            await self.db_session.commit()
            if result.rowcount > 0:
                logger.info("Task updated successfully: %s", task_id)
                return task_data
            else:
                logger.debug("Task not found: %s", task_id)
                raise TaskNotFoundException(f"Task {task_id} not found")
        except Exception as e:
            logger.error("Failed to update task with ID: %s. Error: %s", task_id, e)
            raise DatabaseError("Failed to update task") from e
