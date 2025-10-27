"""Weather service for fetching weather data from external API."""

from __future__ import annotations

import logging

import requests

from backend.config import Config

logger = logging.getLogger(__name__)


class WeatherService:
    """Service for interacting with weather API."""

    @staticmethod
    def get_weather(latitude: float, longitude: float) -> dict | None:
        """Fetch weather data for given coordinates.

        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate

        Returns:
            dict: Weather data or None if request fails
        """
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current_weather": "true",
                "temperature_unit": "celsius",
                "windspeed_unit": "kmh",
            }

            response = requests.get(Config.WEATHER_API_URL, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if "current_weather" not in data:
                logger.error("Invalid weather API response format")
                return None

            current = data["current_weather"]

            return {
                "temperature": current.get("temperature"),
                "windspeed": current.get("windspeed"),
                "winddirection": current.get("winddirection"),
                "weathercode": current.get("weathercode"),
                "time": current.get("time"),
                "latitude": latitude,
                "longitude": longitude,
            }

        except requests.exceptions.RequestException:
            logger.exception("Weather API request failed")
            return None
        except (KeyError, ValueError):
            logger.exception("Error parsing weather data")
            return None

    @staticmethod
    def get_weather_description(weathercode: int) -> str:
        """Get human-readable weather description from WMO code.

        Args:
            weathercode: WMO Weather interpretation code

        Returns:
            str: Weather description
        """
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail",
        }
        return weather_codes.get(weathercode, "Unknown")
