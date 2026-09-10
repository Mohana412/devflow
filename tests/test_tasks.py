from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_task():
    response = client.post(
        "/tasks",
        json={
            "title": "Test CI/CD",
            "description": "Test automated task creation",
            "priority": "HIGH",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Test CI/CD"
    assert data["description"] == "Test automated task creation"
    assert data["priority"] == "HIGH"
    assert data["status"] == "TODO"

def test_get_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_get_task():
    response = client.get("/tasks/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["title"] == "Learn Docker"

def test_update_task():
    response = client.put(
        "/tasks/1",
        json={
            "status": "DONE"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["status"] == "DONE"

def test_get_task_not_found():
    response = client.get("/tasks/99999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_update_task_not_found():
    response = client.put(
        "/tasks/99999",
        json={
            "status": "DONE"
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_delete_task():
    create_response = client.post(
        "/tasks",
        json={
            "title": "Task to Delete",
            "description": "This task will be deleted",
            "priority": "LOW",
        },
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")

    assert delete_response.status_code == 204

    get_response = client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Task not found"}
