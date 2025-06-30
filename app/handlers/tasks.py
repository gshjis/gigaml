from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas.task import Task

from app.core.database import get_db_session

from app.repository import TaskRepository

router = APIRouter(prefix='/tasks', tags=['tasks'])

@router.get('/all', response_model=List[Task])
async def get_tasks(
    task_repo: TaskRepository = Depends(TaskRepository)
):  
    return task_repo.get_all_tasks()


@router.post('/create')
async def create_task(task: Task):
    pass

@router.delete('/delete')
async def delete_task(id_task:int, 
                      task_repo: TaskRepository = Depends(TaskRepository)):
    task_repo.delete_task(id_task)