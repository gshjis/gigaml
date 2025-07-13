# app/handlers/task.py
from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.core.exceptions import InvalidTaskDataError
from app.handlers.dependencies import get_task_service
from app.schemas.task import (TaskSchemaInput, TaskSchemaOutput,
                              TaskSchemaUpdate)
from app.service.task import TaskService

router = APIRouter(prefix="/api/tasks", tags=["Tasks 📑"])

import logging

logger = logging.getLogger(__name__)

@router.get(
    "",
    response_model=list[TaskSchemaOutput],
    summary="Get all tasks",
    responses={
        status.HTTP_200_OK: {
            "description": "List of all active tasks",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "name": "Example task",
                            "pomodoro_count": 4,
                            "category_id": 1,
                        }
                    ]
                }
            },
        }
    },
)
async def get_all_tasks(
    service: TaskService = Depends(get_task_service),
) -> list[TaskSchemaOutput]:
    """
    Retrieve all active tasks.

    Returns:
        List of TaskSchemaOutput objects representing all active tasks
    """
    logger.info("Fetching all tasks")
    tasks = await service.get_all_tasks()
    logger.info("Fetched %s tasks successfully", len(tasks))
    return tasks

@router.post(
    "",
    response_model=TaskSchemaOutput,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    responses={
        status.HTTP_201_CREATED: {"description": "Task created successfully"},
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid task data",
            "content": {
                "application/json": {"example": {
                    "detail": "Invalid pomodoro count"
                }}
            },
        },
    },
)
async def create_task(
    task_data: TaskSchemaInput,
    service: TaskService = Depends(get_task_service)
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
    try:
        logger.info("Creating task with data: %s", task_data)
        return await service.create_task(task_data)
    except InvalidTaskDataError as e:
        logger.error("Invalid task data: %s", e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "Task deleted successfully"
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Task not found",
            "content": {
                "application/json": {"example": {"detail": "Task 123 not found"
                                                 }}
            },
        },
    },
)
async def delete_task(
    task_id: int, service: TaskService = Depends(get_task_service)
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
    await service.delete_task(task_id)
    logger.info("Task deleted successfully: %s", task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch(
    "/{task_id}",
    response_model=TaskSchemaOutput,
    summary="Update a task",
    responses={
        status.HTTP_200_OK: {"description": "Task updated successfully"},
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid update data"},
        status.HTTP_404_NOT_FOUND: {"description": "Task not found"},
    },
)
async def update_task(
    task_id: int,
    update_data: TaskSchemaUpdate,
    service: TaskService = Depends(get_task_service),
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
    return await service.update_task(task_id, update_data)
