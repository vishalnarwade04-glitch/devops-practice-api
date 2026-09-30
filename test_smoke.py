import pytest

BASE_URL = "http://localhost:5000"

def test_health_endpoint_live(page):
    request_context = page.request
    response = request_context.get(f"{BASE_URL}/health")
    assert response.status == 200
    assert response.json()["status"] == "ok"

def test_tasks_endpoint_live(page):
    request_context = page.request
    response = request_context.get(f"{BASE_URL}/tasks")
    assert response.status == 200
    assert isinstance(response.json(), list)

def test_create_task_live(page):
    request_context = page.request
    response = request_context.post(
        f"{BASE_URL}/tasks",
        data={"title": "Smoke test task"}
    )
    assert response.status == 201
    assert response.json()["title"] == "Smoke test task"
