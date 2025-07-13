import pytest
from app.service.task import TaskService
from app.models.task import Task
from app.schemas.task import TaskCreate

@pytest.fixture
def task_service():
    return TaskService()

def test_create_task(task_service):
    task_data = TaskCreate(title="Test Task", description="This is a test task")
    task = task_service.create_task(task_data)
    assert task.title == "Test Task"
    assert task.description == "This is a test task"
    assert isinstance(task, Task)

def test_get_task(task_service):
    task_data = TaskCreate(title="Test Task", description="This is a test task")
    created_task = task_service.create_task(task_data)
    retrieved_task = task_service.get_task(created_task.id)
    assert retrieved_task.title == "Test Task"
    assert retrieved_task.description == "This is a test task"
    assert isinstance(retrieved_task, Task)
