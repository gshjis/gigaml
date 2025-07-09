# app/service/task.py
from typing import List, Optional

from app.core.exceptions import DatabaseError, TaskNotFoundError
from app.models.task import Task
from app.repository.task import TaskRepository
from app.schemas.task import (TaskSchemaInput, TaskSchemaOutput,
                              TaskSchemaUpdate)


class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self.repository = task_repository

    def create_task(self, task_data: TaskSchemaInput) -> TaskSchemaOutput:
        """Создание задачи с валидацией"""
        try:
            task = Task(**task_data.model_dump())
            created_task = self.repository.create(task)
            return TaskSchemaOutput.model_validate(created_task.__dict__)
        except ValueError as e:
            raise DatabaseError("Invalid task data") from e
        except Exception as e:
            raise DatabaseError("Failed to create task") from e

    def get_task(self, task_id: int) -> Optional[TaskSchemaOutput]:
        """Получение задачи по ID"""
        task = self.repository.get(task_id)
        return TaskSchemaOutput.model_validate(task.__dict__) if task else None

    def get_task_or_raise(self, task_id: int) -> TaskSchemaOutput:
        """Получение задачи с проверкой существования"""
        task = self.get_task(task_id)
        if not task:
            raise TaskNotFoundError(f"Task {task_id} not found")
        return task

    def get_all_tasks(self) -> List[TaskSchemaOutput]:
        """Получение всех активных задач"""
        try:
            tasks = self.repository.get_all()
            return [TaskSchemaOutput.model_validate(t.__dict__) for t in tasks]
        except Exception as e:
            raise DatabaseError("Failed to get tasks") from e

    def delete_task(self, task_id: int) -> bool:
        """Удаление задачи"""
        try:
            if not self.repository.delete(task_id):
                raise TaskNotFoundError(f"Task {task_id} not found")
            return True
        except Exception as e:
            if not isinstance(e, TaskNotFoundError):
                raise DatabaseError("Failed to delete task") from e
            raise

    def update_task(
        self, task_id: int, update_data: TaskSchemaUpdate
    ) -> TaskSchemaOutput:
        """Обновление задачи"""
        try:
            task = self.repository.get(task_id)
            if not task:
                raise TaskNotFoundError(f"Task {task_id} not found")

            update_dict = update_data.model_dump(exclude_unset=True)
            for field, value in update_dict.items():
                setattr(task, field, value)

            updated_task = self.repository.update(task)
            return TaskSchemaOutput.model_validate(updated_task.__dict__)
        except ValueError as e:
            raise DatabaseError("Invalid update data") from e
        except Exception as e:
            raise DatabaseError("Failed to update task") from e
