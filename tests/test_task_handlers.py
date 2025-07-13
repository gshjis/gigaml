import pytest
from fastapi.testclient import TestClient
from app.core.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_create_task(client):
    response = client.post("/tasks/", json={"title": "Test Task", "description": "This is a test task"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"

def test_get_task(client):
    response = client.post("/tasks/", json={"title": "Test Task", "description": "This is a test task"})
    assert response.status_code == 200
    task_id = response.json()["id"]
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"
