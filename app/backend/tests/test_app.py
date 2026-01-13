import pytest


def test_health_check(client):
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "ok"
    assert "Backend is running" in data["message"]

