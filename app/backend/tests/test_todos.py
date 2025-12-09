from bson import ObjectId


def _create_todo(client, headers, title="First todo", description="desc"):
    return client.post(
        "/api/todos/",
        json={"title": title, "description": description},
        headers=headers,
    )


def _login_headers(client, username="todoUser", password="secret123"):
    client.post("/api/auth/register", json={"username": username, "password": password})
    login = client.post("/api/auth/login", json={"username": username, "password": password})
    token = login.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_todo(client):
    headers = _login_headers(client)
    resp = _create_todo(client, headers)
    assert resp.status_code == 201
    data = resp.get_json()["todo"]
    assert data["title"] == "First todo"
    assert data["completed"] is False


def test_list_todos(client):
    headers = _login_headers(client)
    _create_todo(client, headers, "A")
    _create_todo(client, headers, "B")
    resp = client.get("/api/todos/", headers=headers)
    assert resp.status_code == 200
    todos = resp.get_json()["todos"]
    assert len(todos) == 2
    titles = {t["title"] for t in todos}
    assert {"A", "B"} == titles


def test_toggle_todo(client):
    headers = _login_headers(client)
    todo = _create_todo(client, headers).get_json()["todo"]
    resp = client.patch(f"/api/todos/{todo['_id']}/toggle", headers=headers)
    assert resp.status_code == 200
    assert resp.get_json()["todo"]["completed"] is True


def test_update_todo(client):
    headers = _login_headers(client)
    todo = _create_todo(client, headers).get_json()["todo"]
    resp = client.put(
        f"/api/todos/{todo['_id']}",
        json={"title": "Updated", "description": "New desc", "completed": True},
        headers=headers,
    )
    assert resp.status_code == 200
    updated = resp.get_json()["todo"]
    assert updated["title"] == "Updated"
    assert updated["description"] == "New desc"
    assert updated["completed"] is True


def test_delete_todo(client):
    headers = _login_headers(client)
    todo = _create_todo(client, headers).get_json()["todo"]
    resp = client.delete(f"/api/todos/{todo['_id']}", headers=headers)
    assert resp.status_code == 200
    # ensure removed
    resp_list = client.get("/api/todos/", headers=headers)
    assert resp_list.status_code == 200
    todos = resp_list.get_json()["todos"]
    assert all(t["_id"] != todo["_id"] for t in todos)


def test_invalid_todo_id(client):
    headers = _login_headers(client)
    resp = client.put(
        "/api/todos/notanid",
        json={"title": "X"},
        headers=headers,
    )
    assert resp.status_code == 400
    assert "Invalid todo ID" in resp.get_json()["error"]

