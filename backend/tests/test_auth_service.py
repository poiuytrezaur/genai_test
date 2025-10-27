"""Unit tests for authentication service."""

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


def test_register_user(app):
    """Test user registration."""
    with app.app_context():
        user = AuthService.register_user("testuser", "test@example.com", "password123")

        assert user is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.check_password("password123")


def test_register_duplicate_username(app):
    """Test registration with duplicate username."""
    with app.app_context():
        AuthService.register_user("testuser", "test1@example.com", "password123")
        user = AuthService.register_user("testuser", "test2@example.com", "password456")

        assert user is None


def test_register_duplicate_email(app):
    """Test registration with duplicate email."""
    with app.app_context():
        AuthService.register_user("testuser1", "test@example.com", "password123")
        user = AuthService.register_user("testuser2", "test@example.com", "password456")

        assert user is None


def test_authenticate_user(app):
    """Test user authentication."""
    with app.app_context():
        AuthService.register_user("testuser", "test@example.com", "password123")
        user = AuthService.authenticate_user("testuser", "password123")

        assert user is not None
        assert user.username == "testuser"


def test_authenticate_invalid_password(app):
    """Test authentication with invalid password."""
    with app.app_context():
        AuthService.register_user("testuser", "test@example.com", "password123")
        user = AuthService.authenticate_user("testuser", "wrongpassword")

        assert user is None


def test_authenticate_nonexistent_user(app):
    """Test authentication with nonexistent user."""
    with app.app_context():
        user = AuthService.authenticate_user("nonexistent", "password123")

        assert user is None


def test_get_user_by_id(app):
    """Test getting user by ID."""
    with app.app_context():
        created_user = AuthService.register_user(
            "testuser", "test@example.com", "password123"
        )
        user = AuthService.get_user_by_id(created_user.id)

        assert user is not None
        assert user.username == "testuser"


def test_get_user_by_username(app):
    """Test getting user by username."""
    with app.app_context():
        AuthService.register_user("testuser", "test@example.com", "password123")
        user = AuthService.get_user_by_username("testuser")

        assert user is not None
        assert user.email == "test@example.com"
