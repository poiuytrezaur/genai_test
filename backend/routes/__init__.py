"""Routes module for API endpoints."""

from backend.routes.auth_routes import auth_bp
from backend.routes.weather_routes import weather_bp

__all__ = ["auth_bp", "weather_bp"]
