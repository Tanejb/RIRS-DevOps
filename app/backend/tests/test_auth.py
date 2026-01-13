def test_register_success(client):
    resp = client.post(
        "/api/auth/register", json={"username": "alice", "password": "password123"}
    )
    assert resp.status_code == 201
    assert resp.get_json()["message"] == "User registered successfully"


def test_register_duplicate_user(client):
    payload = {"username": "bob", "password": "password123"}
    client.post("/api/auth/register", json=payload)
    resp = client.post("/api/auth/register", json=payload)
    assert resp.status_code == 400
    assert "already exists" in resp.get_json()["error"]


def test_login_success(client):
    client.post("/api/auth/register", json={"username": "carol", "password": "password123"})
    resp = client.post("/api/auth/login", json={"username": "carol", "password": "password123"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert "access_token" in data
    assert data["user"]["username"] == "carol"


def test_login_invalid_credentials(client):
    client.post("/api/auth/register", json={"username": "dave", "password": "password123"})
    resp = client.post("/api/auth/login", json={"username": "dave", "password": "badpassword"})
    assert resp.status_code == 401
    assert "Invalid credentials" in resp.get_json()["error"]


def test_profile_requires_token(client):
    resp = client.get("/api/auth/profile")
    assert resp.status_code == 401


def test_profile_with_token(client):
    client.post("/api/auth/register", json={"username": "erin", "password": "password123"})
    login = client.post("/api/auth/login", json={"username": "erin", "password": "password123"})
    token = login.get_json()["access_token"]
    resp = client.get("/api/auth/profile", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.get_json()["username"] == "erin"


def test_register_short_username(client):
    resp = client.post("/api/auth/register", json={"username": "ab", "password": "password123"})
    assert resp.status_code == 400
    assert "at least 3 characters" in resp.get_json()["error"]


def test_register_long_username(client):
    resp = client.post("/api/auth/register", json={"username": "a" * 51, "password": "password123"})
    assert resp.status_code == 400
    assert "less than 50 characters" in resp.get_json()["error"]


def test_register_short_password(client):
    resp = client.post("/api/auth/register", json={"username": "user1", "password": "short"})
    assert resp.status_code == 400
    assert "at least 6 characters" in resp.get_json()["error"]


def test_register_long_password(client):
    resp = client.post("/api/auth/register", json={"username": "user2", "password": "a" * 129})
    assert resp.status_code == 400
    assert "less than 128 characters" in resp.get_json()["error"]


def test_register_missing_fields(client):
    resp = client.post("/api/auth/register", json={})
    assert resp.status_code == 400
    assert "required" in resp.get_json()["error"]


def test_login_missing_fields(client):
    resp = client.post("/api/auth/login", json={})
    assert resp.status_code == 400
    assert "required" in resp.get_json()["error"]


def test_login_empty_username(client):
    resp = client.post("/api/auth/login", json={"username": "", "password": "password123"})
    assert resp.status_code == 400
    assert "required" in resp.get_json()["error"]


def test_profile_user_not_found(client, app):
    # Create a token for a user that doesn't exist in DB
    from flask_jwt_extended import create_access_token
    with app.app_context():
        token = create_access_token(identity="nonexistent")
    resp = client.get("/api/auth/profile", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 404
    assert "not found" in resp.get_json()["error"]

