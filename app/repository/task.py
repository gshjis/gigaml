from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from fastapi import Depends

from app.models import Task
from app.core.database import get_db_session


class TaskRepository:

    def __init__(self, db_session: Session = Depends(get_db_session)):
        self.db_session = db_session
    
    def delete_task(self, task_id: int) -> None:
        stmt = delete(Task).where(Task.id == task_id)
        self.db_session.execute(stmt)
        self.db_session.commit() 

    def get_all_tasks(self) -> list[Task]:
        data = self.db_session.scalars(select(Task)).all()
        return data
    
    def create_task(self, task: Task):
        pass




