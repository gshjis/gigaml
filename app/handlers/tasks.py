from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.task import Task
from app.repository import TaskRepository
from app.schemas.task import TaskSchema  # Рекомендуется разделить схемы

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get(
    "/all",
    response_model=List[TaskSchema],
    summary="Get all tasks",
    description="Returns list of all tasks",
)
async def get_all_tasks(task_repo: TaskRepository = Depends(TaskRepository)):
    """Get all tasks from database"""
    return task_repo.get_all()


@router.post(
    "/create",
    response_model=TaskSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create new task",
    responses={
        400: {"description": "Invalid data"},
        201: {"description": "Task created successfully"},
    },
)
async def create_task(
    task_data: TaskSchema,  # Лучше использовать отдельную схему для создания
    task_repo: TaskRepository = Depends(TaskRepository),
):
    """Create new task in database"""
    try:
        task = Task(**task_data.model_dump())
        created_task = task_repo.create(task)
        return created_task
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Failed to create task", "details": str(exc)},
        )


@router.delete(
    "/delete/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete task by ID",
    responses={
        204: {"description": "Task deleted successfully"},
        404: {"description": "Task not found"},
        400: {"description": "Invalid request"},
    },
)
async def delete_task(
    task_id: int, task_repo: TaskRepository = Depends(TaskRepository)
):
    """Delete task by ID"""
    try:
        if not task_repo.delete(task_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": f"Task with ID {task_id} not found"},
            )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Failed to delete task", "details": str(exc)},
        )


@router.patch("/patch")
async def patch_task(task_repo: TaskRepository = Depends(TaskRepository)):
    pass
