import pytest

def test_register_user(client):
    response = client.post("/api/v1/register", json={
        "email": "testuser@example.com",
        "password": "testpass123"
    })
    assert response.status_code in (200, 201)

