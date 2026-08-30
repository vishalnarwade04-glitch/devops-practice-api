import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"

def test_get_tasks(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_create_task(client):
    response = client.post("/tasks", json={"title": "Test task"})
    assert response.status_code == 201
    assert response.get_json()["title"] == "Test task"

def test_create_task_missing_title(client):
    response = client.post("/tasks", json={})
    assert response.status_code == 400

def test_delete_task_not_found(client):
    response = client.delete("/tasks/9999")
    assert response.status_code == 404
