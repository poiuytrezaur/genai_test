"""Application configuration settings."""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Config:
    """Application configuration class."""

    # Security: Require SECRET_KEY in production
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        if os.environ.get("FLASK_ENV") == "production":
            print("ERROR: SECRET_KEY must be set in production", file=sys.stderr)
            sys.exit(1)
        # Only use default in development
        SECRET_KEY = "dev-secret-key-change-in-production"

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'weather_app.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Weather API configuration
    WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

    # Session configuration
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
