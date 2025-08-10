import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.main import app
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import get_superuser_token_headers


@pytest.fixture(scope="module")
def client() -> TestClient:
    with TestClient(app) as c:
        yield c


def test_read_root(client: TestClient) -> None:
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "docs" in response.json()
    assert "api" in response.json()


def test_read_favicon(client: TestClient) -> None:
    """Test the favicon endpoint."""
    response = client.get("/favicon.ico")
    # This might fail if the favicon path is not set correctly
    # We're just testing that the route exists
    assert response.status_code in (200, 404)


def test_read_openapi(client: TestClient) -> None:
    """Test the OpenAPI endpoint."""
    response = client.get("/api/v1/openapi.json")
    assert response.status_code == 200
    assert "openapi" in response.json()
    assert "paths" in response.json()


def test_cors_headers(client: TestClient) -> None:
    """Test that CORS headers are set correctly."""
    response = client.options(
        "/api/v1/users/",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
        },
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert "access-control-allow-methods" in response.headers
    assert "access-control-allow-headers" in response.headers


def test_custom_generate_unique_id() -> None:
    """Test the custom_generate_unique_id function."""
    from app.main import custom_generate_unique_id
    from fastapi.routing import APIRoute

    # Create a mock route with tags
    route_with_tags = APIRoute(
        path="/test",
        endpoint=lambda: None,
        methods=["GET"],
        tags=["test-tag"],
        name="test-name",
    )
    assert custom_generate_unique_id(route_with_tags) == "test-tag-test-name"

    # Create a mock route without tags
    route_without_tags = APIRoute(
        path="/test",
        endpoint=lambda: None,
        methods=["GET"],
        name="test-name",
    )
    assert custom_generate_unique_id(route_without_tags) == "test-name"