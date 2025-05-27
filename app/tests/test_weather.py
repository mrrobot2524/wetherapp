import pytest

def test_root_redirect(client):
    response = client.get("/")
    assert response.status_code in (200, 307)

