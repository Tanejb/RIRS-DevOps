import os
import pytest
import mongomock

# Patch models before app import so blueprints pick up mocked DB
import backend.models as models

# Ensure JWT secret for tests
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key")

# Replace real Mongo client with in-memory mongomock
models.client = mongomock.MongoClient()
models.db_instance = models.client[models.DATABASE_NAME]
models.users_collection = models.db_instance.users
models.todos_collection = models.db_instance.todos
models.db = models.Database()

from backend.app import create_app  # noqa: E402


@pytest.fixture
def app():
    app = create_app()
    app.config.update({"TESTING": True})
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def clean_db():
    """Clean database before each test."""
    yield
    # Clean collections after each test
    models.users_collection.delete_many({})
    models.todos_collection.delete_many({})


@pytest.fixture
def auth_headers(client):
    """Register and login a user, return Authorization headers."""
    username = "testuser"
    password = "secret123"

    # register
    client.post("/api/auth/register", json={"username": username, "password": password})
    # login
    login_resp = client.post(
        "/api/auth/login", json={"username": username, "password": password}
    )
    token = login_resp.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

