"""Main Flask application factory and entry point."""

from __future__ import annotations

import logging
import os

from flask import Flask, render_template

from backend.config import Config
from backend.models.user import db
from backend.routes import auth_bp, weather_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_app(config_class: type = Config) -> Flask:
    """Create and configure the Flask application.

    Args:
        config_class: Configuration class to use

    Returns:
        Flask: Configured Flask application
    """
    app = Flask(
        __name__,
        template_folder="../frontend/templates",
        static_folder="../frontend/static",
    )

    # Load configuration
    app.config.from_object(config_class)

    # Initialize database
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(weather_bp)

    # Create database tables
    with app.app_context():
        db.create_all()
        logger.info("Database tables created")

    # Frontend routes
    @app.route("/")
    def index() -> str:
        """Render the main page."""
        return render_template("index.html")

    @app.route("/login")
    def login_page() -> str:
        """Render the login page."""
        return render_template("login.html")

    @app.route("/register")
    def register_page() -> str:
        """Render the registration page."""
        return render_template("register.html")

    @app.route("/weather")
    def weather_page() -> str:
        """Render the weather page."""
        return render_template("weather.html")

    # Health check endpoint
    @app.route("/health")
    def health() -> tuple[dict[str, str], int]:
        """Health check endpoint for monitoring."""
        return {"status": "healthy", "version": "1.0.0"}, 200

    logger.info("Flask application created successfully")
    return app


def main() -> None:
    """Run the Flask application."""
    app = create_app()
    port = int(os.environ.get("PORT", "5000"))
    debug = os.environ.get("FLASK_DEBUG", "False").lower() == "true"

    logger.info("Starting Flask application on port %d", port)
    app.run(host="0.0.0.0", port=port, debug=debug)  # noqa: S104


if __name__ == "__main__":
    main()
