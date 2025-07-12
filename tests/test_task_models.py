import pytest
from app.models.task import Task
from app.schemas.task import TaskCreate

def test_task_model():
    task_data = TaskCreate(title="Test Task", description="This is a test task")
    task = Task(**task_data.dict())
    assert task.title == "Test Task"
    assert task.description == "This is a test task"
    assert isinstance(task, Task)
