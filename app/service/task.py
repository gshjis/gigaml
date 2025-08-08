import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from app.core.exceptions import DatabaseError, TaskNotFoundException
from app.domain.task import TaskData
from app.repository.task import TaskRepository

logger = logging.getLogger(__name__)


class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self.repository = task_repository

    async def create_task(
        self,
        name: str,
        description: Optional[str],
        pomodoro_count: int,
        category_id: int,
        owner_id: int,
    ) -> Dict[str, Any]:
        """Создание задачи с валидацией

        Args:
            name (str): Название задачи
            description (Optional[str]): Описание задачи
            pomodoro_count (int): Количество помодоро
            category_id (int): ID категории
            owner_id (int): ID владельца задачи

        Returns:
            Dict[str, Any]: Данные созданной задачи

        Raises:
            DatabaseError: Если данные задачи некорректны или произошла ошибка при создании задачи
        """
        try:
            task = await self.repository.create(
                TaskData(
                    task_id=12,
                    name=name,
                    pomodoro_count=pomodoro_count,
                    category_id=category_id,
                    description=description,
                    owner_id=owner_id,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )
            )
            return TaskData(
                task_id=task.task_id,
                name=task.name,
                description=task.description,
                pomodoro_count=task.pomodoro_count,
                category_id=task.category_id,
                owner_id=task.owner_id,
                created_at=task.created_at,
                updated_at=task.updated_at,
            ).__dict__
        except ValueError as e:
            logger.error("Invalid task data: %s", e)
            raise DatabaseError("Invalid task data") from e
        except Exception as e:
            logger.error("Failed to create task: %s", e)
            raise DatabaseError("Failed to create task") from e

    async def get_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Получение задачи по ID

        Args:
            task_id (int): ID задачи

        Returns:
            Optional[Dict[str, Any]]: Данные задачи или None, если задача не найдена

        Raises:
            TaskNotFoundException: Если задача не найдена
        """
        logger.info("Fetching task with ID: %s", task_id)
        task = await self.repository.get_task_by_id(task_id)
        if not task:
            logger.debug("Task not found: %s", task_id)
            raise TaskNotFoundException(f"Task {task_id} not found")
        return TaskData(
            task_id=task.task_id,
            name=task.name,
            description=task.description,
            pomodoro_count=task.pomodoro_count,
            category_id=task.category_id,
            owner_id=task.owner_id,
            created_at=task.created_at,
            updated_at=task.updated_at,
        ).__dict__

    async def delete_task(self, task_id: int, user_id: int) -> bool:
        """Мягкое удаление задачи

        Args:
            task_id (int): ID задачи
            user_id (int): ID пользователя

        Returns:
            bool: True, если задача успешно удалена, иначе False

        Raises:
            TaskNotFoundException: Если задача не найдена или не принадлежит пользователю
            DatabaseError: Если произошла ошибка при удалении задачи
        """
        try:
            logger.info("Deleting task with ID: %s for user ID: %s", task_id, user_id)
            task = await self.repository.get_task_by_id(task_id)
            if not task:
                logger.error("Task not found: %s", task_id)
                raise TaskNotFoundException(f"Task {task_id} not found")

            if task.owner_id != user_id:
                logger.error("Task not found: %s", task_id)
                raise TaskNotFoundException(f"Task {task_id} not found")

            if not await self.repository.delete_task(task_id, hard_delete=True):
                logger.error("Task not found: %s", task_id)
                raise TaskNotFoundException(f"Task {task_id} not found")
            logger.info("Task deleted successfully: %s", task_id)
            return True
        except TaskNotFoundException:
            raise
        except Exception as e:
            logger.error("Failed to delete task: %s", e)
            raise DatabaseError("Failed to delete task") from e

    async def get_tasks_by_user_id(
        self, user_id: int, include_deleted: bool = False
    ) -> List[Dict[str, Any]]:
        """Получить задачи пользователя по user_id с учетом флага soft delete.

        Args:
            user_id (int): ID пользователя
            include_deleted (bool, optional): Включать удаленные задачи. Defaults to False.

        Returns:
            List[Dict[str, Any]]: Список задач пользователя

        Raises:
            DatabaseError: Если произошла ошибка при получении задач
        """
        try:
            logger.info(
                "Fetching tasks for user ID: %s with include_deleted: %s",
                user_id,
                include_deleted,
            )
            tasks = await self.repository.get_tasks_by_user_id(user_id, include_deleted)
            return [
                TaskData(
                    task_id=task.task_id,
                    name=task.name,
                    description=task.description,
                    pomodoro_count=task.pomodoro_count,
                    category_id=task.category_id,
                    owner_id=task.owner_id,
                    created_at=task.created_at,
                    updated_at=task.updated_at,
                ).__dict__
                for task in tasks
            ]
        except Exception as e:
            logger.error("Failed to fetch tasks for user ID: %s. Error: %s", user_id, e)
            raise DatabaseError("Failed to fetch tasks for user") from e

    async def update_task(
        self,
        task_id: int,
        owner_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        pomodoro_count: Optional[int] = None,
        category_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Обновление задачи

        Args:
            task_id (int): ID задачи
            owner_id (int): ID владельца задачи
            name (Optional[str], optional): Новое название задачи. Defaults to None.
            description (Optional[str], optional): Новое описание задачи. Defaults to None.
            pomodoro_count (Optional[int], optional): Новое количество помодоро. Defaults to None.
            category_id (Optional[int], optional): Новый ID категории. Defaults to None.

        Returns:
            Dict[str, Any]: Данные обновленной задачи

        Raises:
            TaskNotFoundException: Если задача не найдена
            DatabaseError: Если произошла ошибка при обновлении задачи
        """
        try:
            logger.info("Updating task %s with data: %s", task_id, locals())
            task = await self.repository.get_task_by_id(task_id)
            if not task:
                logger.error("Task not found: %s", task_id)
                raise TaskNotFoundException(f"Task {task_id} not found")

            update_data = {
                k: v for k, v in locals().items() if v is not None and k != "task_id"
            }
            for field, value in update_data.items():
                setattr(task, field, value)

            updated_task = await self.repository.update_task(
                task_data=task, task_id=task_id
            )
            return TaskData(
                task_id=updated_task.task_id,
                name=updated_task.name,
                description=updated_task.description,
                pomodoro_count=updated_task.pomodoro_count,
                category_id=updated_task.category_id,
                owner_id=updated_task.owner_id,
                created_at=task.created_at,
                updated_at=task.updated_at,
            ).__dict__
        except ValueError as e:
            logger.error("Invalid update data: %s", e)
            raise DatabaseError("Invalid update data") from e
        except Exception as e:
            logger.error("Failed to update task: %s", e)
            raise DatabaseError("Failed to update task") from e
