import pytest
from app import app
from fastapi import status
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def test_root_returns_200(client: TestClient):
    response = client.get("/")
    content_type: str | None = response.headers.get("Content-Type")
    assert content_type is not None
    assert content_type.startswith("text/html")
    assert response.status_code == status.HTTP_200_OK


def test_spa_prefix_matches_existing_route_returns_200(client: TestClient):
    response = client.get("/test")
    content_type: str | None = response.headers.get("Content-Type")
    assert content_type is not None
    assert content_type.startswith("text/html")
    assert response.status_code == status.HTTP_200_OK


def test_non_spa_unknown_path_returns_404(client: TestClient):
    response = client.get("/non-existent-path")
    content_type: str | None = response.headers.get("Content-Type")
    assert content_type is not None
    assert content_type.startswith("text/html")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_static_file_served_correctly(client: TestClient):
    response = client.get("/test.html")
    content_type: str | None = response.headers.get("Content-Type")
    assert content_type is not None
    assert content_type.startswith("text/html")
    assert response.status_code == status.HTTP_200_OK


def test_head_request_returns_200(client: TestClient):
    client = TestClient(app)
    response = client.head("/")
    assert response.status_code == status.HTTP_200_OK
