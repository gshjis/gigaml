from fastapi import APIRouter
from fixtures import (
    tasks as fixture_tasks,
    categories as fixture_categories
    )

router = APIRouter(prefix='/tasks', tags=['tasks'])

@router.get('/all')
async def get_tasks():
    return {'tasks': fixture_tasks}

@router.post('/')
async def create_task(name: str):
    return {'message': 'Task created.'} 