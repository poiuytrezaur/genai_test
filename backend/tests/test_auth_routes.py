"""Unit tests for authentication routes."""

import json

import pytest

from backend.app import create_app
from backend.models.user import db
from backend.services import AuthService


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


def test_register_route(client):
    """Test registration endpoint."""
    response = client.post(
        "/api/auth/register",
        data=json.dumps(
            {
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123",
            }
        ),
        content_type="application/json",
    )

    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["message"] == "User registered successfully"
    assert data["user"]["username"] == "testuser"


def test_register_missing_fields(client):
    """Test registration with missing fields."""
    response = client.post(
        "/api/auth/register",
        data=json.dumps({"username": "testuser", "email": "test@example.com"}),
        content_type="application/json",
    )

    assert response.status_code == 400


def test_register_short_username(client):
    """Test registration with short username."""
    response = client.post(
        "/api/auth/register",
        data=json.dumps(
            {"username": "ab", "email": "test@example.com", "password": "password123"}
        ),
        content_type="application/json",
    )

    assert response.status_code == 400


def test_register_short_password(client):
    """Test registration with short password."""
    response = client.post(
        "/api/auth/register",
        data=json.dumps(
            {"username": "testuser", "email": "test@example.com", "password": "12345"}
        ),
        content_type="application/json",
    )

    assert response.status_code == 400


def test_login_route(client, app):
    """Test login endpoint."""
    with app.app_context():
        AuthService.register_user("testuser", "test@example.com", "password123")

    response = client.post(
        "/api/auth/login",
        data=json.dumps({"username": "testuser", "password": "password123"}),
        content_type="application/json",
    )

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Login successful"


def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    response = client.post(
        "/api/auth/login",
        data=json.dumps({"username": "testuser", "password": "wrongpassword"}),
        content_type="application/json",
    )

    assert response.status_code == 401


def test_logout_route(client):
    """Test logout endpoint."""
    response = client.post("/api/auth/logout")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Logout successful"


def test_get_current_user_authenticated(client, app):
    """Test getting current user when authenticated."""
    with app.app_context():
        AuthService.register_user("testuser", "test@example.com", "password123")

    with client.session_transaction() as session:
        session["user_id"] = 1
        session["username"] = "testuser"

    response = client.get("/api/auth/me")

    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["user"]["username"] == "testuser"


def test_get_current_user_not_authenticated(client):
    """Test getting current user when not authenticated."""
    response = client.get("/api/auth/me")

    assert response.status_code == 401
