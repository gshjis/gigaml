from fastapi import APIRouter
from app.schemas.task import Task
from typing import List
from app.core.database import get_db_connection

router = APIRouter(prefix='/tasks', tags=['tasks'])

@router.get('/all', response_model=List[Task])
def get_tasks():
    connection = get_db_connection() 
    cursor = connection.cursor()
        
    # Получаем данные
    cursor.execute("SELECT * FROM Tasks")
    columns = [column[0] for column in cursor.description]  # Получаем названия колонок
    tasks = [dict(zip(columns, row)) for row in cursor.fetchall()]  # Конвертируем в словари
    
    connection.close()
    return tasks

@router.post('/')
def create_task(task: Task):
    connection = get_db_connection() 
    cursor = connection.cursor()
    
    # Убираем id из INSERT, если он автоинкрементный
    cursor.execute(
        "INSERT INTO Tasks (id, name, pomodoro_count, category_id) VALUES (?, ?, ?, ?)",
        (task.id, task.name, task.pomodoro_count, task.category_id)
    )
    connection.commit()
    
    task_id = cursor.lastrowid
    cursor.execute("SELECT * FROM Tasks WHERE Tasks.id == ?", (task_id,))
    columns = [column[0] for column in cursor.description]
    new_task = dict(zip(columns, cursor.fetchone()))  # Конвертируем в словарь
    
    connection.close()
    return new_task