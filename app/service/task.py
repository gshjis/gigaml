from typing import List, Optional
import logging
from pydantic import ValidationError
from app.utils.cache import cache_result
from app.core.exceptions import DatabaseError, TaskNotFoundError
from app.models.task import Task
from app.repository.task import TaskRepository
from app.schemas.task import TaskSchemaInput, TaskSchemaOutput, TaskSchemaUpdate

logger = logging.getLogger(__name__)

class TaskService:
    def __init__(self, task_repository: TaskRepository):
        # 
        self.repository = task_repository

    async def create_task(self, task_data: TaskSchemaInput) -> TaskSchemaOutput:
        """Создание задачи с валидацией"""
        try:
            logger.info("Creating task with data: %s", task_data.model_dump())
            task = await self.repository.create(Task(**task_data.model_dump()))
            logger.info("Task created successfully with ID: %s", task.id)
            return TaskSchemaOutput.model_validate(task, from_attributes=True)
        except ValueError as e:
            logger.error("Invalid task data: %s", e)
            raise DatabaseError("Invalid task data") from e
        except Exception as e:
            logger.error("Failed to create task: %s", e)
            raise DatabaseError("Failed to create task") from e

    @cache_result(expiration_time=300)
    async def get_task(self, task_id: int) -> Optional[TaskSchemaOutput]:
        """Получение задачи по ID с кешированием"""
        logger.info("Fetching task with ID: %s", task_id)
        task = await self.repository.get(task_id)
        if not task:
            logger.debug("Task not found: %s", task_id)
            return None
        logger.info("Task fetched successfully: %s", task_id)
        return TaskSchemaOutput.model_validate(task, from_attributes=True)

    async def get_task_or_raise(self, task_id: int) -> TaskSchemaOutput:
        """Получение задачи с проверкой существования"""
        task = await self.get_task(task_id)        
        if not task:
            logger.error("Task not found: %s", task_id)
            raise TaskNotFoundError(f"Task {task_id} not found")
        return task

    # @cache_result(expiration_time=300)
    async def get_all_tasks(self) -> List[dict]:
        """Получение всех активных задач с кешированием"""
        try:
            logger.info("Fetching all tasks")
            tasks = await self.repository.get_all()
            logger.info("Fetched %s tasks successfully", len(tasks))
            
            # Возвращаем словари для кеширования
            return [
                TaskSchemaOutput.model_validate(task, from_attributes=True).model_dump()
                for task in tasks
            ]
        except Exception as e:
            logger.error("Error fetching tasks: %s", e)
            raise DatabaseError("Failed to get tasks") from e

    async def delete_task(self, task_id: int) -> bool:
        """Мягкое удаление задачи"""
        try:
            logger.info("Deleting task with ID: %s", task_id)
            if not await self.repository.delete(task_id, hard_delete=True):
                logger.error("Task not found: %s", task_id)
                raise TaskNotFoundError(f"Task {task_id} not found")
            logger.info("Task deleted successfully: %s", task_id)
            return True
        except TaskNotFoundError:
            raise
        except Exception as e:
            logger.error("Failed to delete task: %s", e)
            raise DatabaseError("Failed to delete task") from e

    @cache_result(expiration_time=300)
    async def update_task(
        self, task_id: int, update_data: TaskSchemaUpdate
    ) -> dict:
        """Обновление задачи с кешированием"""
        try:
            logger.info("Updating task %s with data: %s", task_id, update_data.model_dump())
            task = await self.repository.get(task_id)
            if not task:
                logger.error("Task not found: %s", task_id)
                raise TaskNotFoundError(f"Task {task_id} not found")

            update_dict = update_data.model_dump(exclude_unset=True)
            for field, value in update_dict.items():
                setattr(task, field, value)

            updated_task = await self.repository.update(task)
            logger.info("Task updated successfully: %s", task_id)
            return TaskSchemaOutput.model_validate(updated_task, from_attributes=True).model_dump()
        except ValueError as e:
            logger.error("Invalid update data: %s", e)
            raise DatabaseError("Invalid update data") from e
        except Exception as e:
            logger.error("Failed to update task: %s", e)
            raise DatabaseError("Failed to update task") from e
    
    