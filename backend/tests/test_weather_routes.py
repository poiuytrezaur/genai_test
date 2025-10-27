"""Unit tests for weather routes."""

import json

import pytest

from backend.app import create_app
from backend.database import db
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


@pytest.fixture
def authenticated_client(client, app):
    """Create authenticated test client."""
    with app.app_context():
        AuthService.register_user("testuser", "test@example.com", "password123")

    with client.session_transaction() as session:
        session["user_id"] = 1
        session["username"] = "testuser"

    return client


def test_get_weather_not_authenticated(client):
    """Test weather endpoint without authentication."""
    response = client.get("/api/weather/current?latitude=40.7128&longitude=-74.0060")

    assert response.status_code == 401
    data = json.loads(response.data)
    assert "error" in data


def test_get_weather_missing_latitude(authenticated_client):
    """Test weather endpoint with missing latitude."""
    response = authenticated_client.get("/api/weather/current?longitude=-74.0060")

    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data


def test_get_weather_missing_longitude(authenticated_client):
    """Test weather endpoint with missing longitude."""
    response = authenticated_client.get("/api/weather/current?latitude=40.7128")

    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data


def test_get_weather_invalid_latitude(authenticated_client):
    """Test weather endpoint with invalid latitude."""
    response = authenticated_client.get(
        "/api/weather/current?latitude=100&longitude=-74.0060"
    )

    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data
    assert "Latitude" in data["error"]


def test_get_weather_invalid_longitude(authenticated_client):
    """Test weather endpoint with invalid longitude."""
    response = authenticated_client.get(
        "/api/weather/current?latitude=40.7128&longitude=200"
    )

    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data
    assert "Longitude" in data["error"]


def test_get_weather_success(authenticated_client):
    """Test successful weather data fetch."""
    response = authenticated_client.get(
        "/api/weather/current?latitude=40.7128&longitude=-74.0060"
    )

    # The response could be 200 (success) or 503 (API unavailable)
    assert response.status_code in [200, 503]

    data = json.loads(response.data)

    if response.status_code == 200:
        assert "weather" in data
        weather = data["weather"]
        assert "temperature" in weather
        assert "latitude" in weather
        assert "longitude" in weather
        assert weather["latitude"] == 40.7128
        assert weather["longitude"] == -74.006
    else:
        assert "error" in data
