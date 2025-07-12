import pytest
from app.repository.task import TaskRepository
from app.models.task import Task
from app.schemas.task import TaskCreate

@pytest.fixture
def task_repository():
    return TaskRepository()

def test_add_task(task_repository):
    task_data = TaskCreate(title="Test Task", description="This is a test task")
    task = task_repository.add_task(task_data)
    assert task.title == "Test Task"
    assert task.description == "This is a test task"
    assert isinstance(task, Task)

def test_get_task_by_id(task_repository):
    task_data = TaskCreate(title="Test Task", description="This is a test task")
    created_task = task_repository.add_task(task_data)
    retrieved_task = task_repository.get_task_by_id(created_task.id)
    assert retrieved_task.title == "Test Task"
    assert retrieved_task.description == "This is a test task"
    assert isinstance(retrieved_task, Task)
