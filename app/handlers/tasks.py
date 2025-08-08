import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.core.dependencies import get_current_user, get_task_service
from app.models.user import User
from app.schemas.task import TaskSchemaInput, TaskSchemaOutput, TaskSchemaUpdate
from app.service.task import TaskService

router = APIRouter(prefix="/api/tasks", tags=["Tasks 📑"])

logger = logging.getLogger(__name__)


@router.get(
    "",
    response_model=list[TaskSchemaOutput],
    summary="Get all tasks",
    description="""Этот маршрут позволяет получить все активные задачи.
    В случае успешного получения возвращается список задач.""",
    status_code=status.HTTP_200_OK,
)
async def get_all_tasks(
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[TaskService, Depends(get_task_service)],
) -> list[TaskSchemaOutput]:
    """
    Retrieve all active tasks.

    Returns:
        List of TaskSchemaOutput objects representing all active tasks
    """
    logger.info("Fetching all tasks")
    tasks = await service.get_tasks_by_user_id(user_id=user.ID)
    logger.info("Fetched %s tasks successfully", len(tasks))

    return [TaskSchemaOutput(**task) for task in tasks]


@router.post(
    "",
    response_model=TaskSchemaOutput,
    summary="Создание новой задачи",
    description="""Этот маршрут позволяет создать новую задачу.
    В случае успешного создания возвращается информация о созданной задаче.""",
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    task_data: TaskSchemaInput,
    service: Annotated[TaskService, Depends(get_task_service)],
    user: Annotated[User, Depends(get_current_user)],
) -> TaskSchemaOutput:
    """
    Create a new task.

    Args:
        task_data: Task input data

    Returns:
        Newly created task data

    Raises:
        HTTPException: If input data is invalid
    """
    logger.info("Creating task with data: %s", task_data)
    created_task = await service.create_task(
        name=task_data.name,
        description=task_data.description,
        pomodoro_count=task_data.pomodoro_count,
        category_id=task_data.category_id,
        owner_id=user.ID,
    )
    return TaskSchemaOutput(**created_task)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаление задачи",
    description="""Этот маршрут позволяет удалить задачу по ID.
    В случае успешного удаления возвращается пустой ответ с кодом 204.""",
)
async def delete_task(
    task_id: int,
    service: Annotated[TaskService, Depends(get_task_service)],
    user: Annotated[User, Depends(get_current_user)],
) -> Response:
    """
    Delete a task by ID.

    Args:
        task_id: ID of the task to delete

    Returns:
        Empty response with 204 status code

    Raises:
        HTTPException: If task is not found
    """
    logger.info("Deleting task with ID: %s", task_id)
    await service.delete_task(task_id, user_id=user.ID)
    logger.info("Task deleted successfully: %s", task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch(
    "/{task_id}",
    response_model=TaskSchemaOutput,
    summary="Обновление задачи",
    description="""Этот маршрут позволяет частично обновить задачу.
    В случае успешного обновления возвращается обновленная информация о задаче.""",
    status_code=status.HTTP_200_OK,
)
async def update_task(
    task_id: int,
    update_data: TaskSchemaUpdate,
    service: Annotated[TaskService, Depends(get_task_service)],
    user: Annotated[User, Depends(get_current_user)],
) -> TaskSchemaOutput:
    """
    Partially update a task.

    Args:
        task_id: ID of the task to update
        update_data: Fields to update

    Returns:
        Updated task data

    Raises:
        HTTPException: If task not found or invalid data
    """
    logger.info("Updating task with ID: %s and data: %s", task_id, update_data)
    updated_task = await service.update_task(
        task_id=task_id,
        owner_id=user.ID,
        name=update_data.name,
        description=update_data.description,
        pomodoro_count=update_data.pomodoro_count,
        category_id=update_data.category_id,
    )
    return TaskSchemaOutput(**updated_task)
