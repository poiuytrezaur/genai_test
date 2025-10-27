"""Weather routes for fetching weather data."""

from __future__ import annotations

import logging
from typing import Any

from flask import Blueprint, jsonify, request, session

from backend.services import WeatherService

logger = logging.getLogger(__name__)

weather_bp = Blueprint("weather", __name__, url_prefix="/api/weather")

# Constants for validation
MIN_LATITUDE = -90
MAX_LATITUDE = 90
MIN_LONGITUDE = -180
MAX_LONGITUDE = 180


@weather_bp.route("/current", methods=["GET"])
def get_current_weather() -> tuple[Any, int]:  # noqa: PLR0911
    """Get current weather for given coordinates.

    Query parameters:
        latitude: float - Latitude coordinate
        longitude: float - Longitude coordinate

    Returns:
        JSON response with weather data or error message
    """
    try:
        # Check authentication
        if not session.get("user_id"):
            return jsonify({"error": "Authentication required"}), 401

        latitude = request.args.get("latitude", type=float)
        longitude = request.args.get("longitude", type=float)

        if latitude is None or longitude is None:
            return jsonify({"error": "Latitude and longitude are required"}), 400

        # Validate coordinate ranges
        if not (MIN_LATITUDE <= latitude <= MAX_LATITUDE):
            return (
                jsonify({"error": "Latitude must be between -90 and 90"}),
                400,
            )

        if not (MIN_LONGITUDE <= longitude <= MAX_LONGITUDE):
            return (
                jsonify({"error": "Longitude must be between -180 and 180"}),
                400,
            )

        weather_data = WeatherService.get_weather(latitude, longitude)

        if not weather_data:
            return jsonify({"error": "Failed to fetch weather data"}), 503

        # Add weather description
        weathercode = weather_data.get("weathercode")
        if weathercode is not None:
            weather_data["description"] = WeatherService.get_weather_description(
                weathercode
            )

        return jsonify({"weather": weather_data}), 200

    except Exception:
        logger.exception("Weather fetch error")
        return jsonify({"error": "Internal server error"}), 500
