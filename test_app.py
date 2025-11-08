import pytest
from app import app


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_hello(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello" in response.data


def test_db(client):
    response = client.get("/db")
    assert response.status_code == 200
    assert b"not set" in response.data


def test_version(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert b"version" in response.data
