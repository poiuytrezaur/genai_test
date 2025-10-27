"""Unit tests for weather service."""

from unittest.mock import Mock, patch

import pytest
import requests

from backend.services import WeatherService


@patch("backend.services.weather_service.requests.get")
def test_get_weather_success(mock_get):
    """Test successful weather data fetch."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "current_weather": {
            "temperature": 20.5,
            "windspeed": 15.0,
            "winddirection": 180,
            "weathercode": 0,
            "time": "2025-10-27T14:00",
        }
    }
    mock_get.return_value = mock_response

    weather = WeatherService.get_weather(40.7128, -74.0060)

    assert weather is not None
    assert weather["temperature"] == 20.5
    assert weather["windspeed"] == 15.0
    assert weather["latitude"] == 40.7128
    assert weather["longitude"] == -74.0060


@patch("backend.services.weather_service.requests.get")
def test_get_weather_api_error(mock_get):
    """Test weather fetch with API error."""
    mock_get.side_effect = requests.exceptions.RequestException("API error")

    weather = WeatherService.get_weather(40.7128, -74.0060)

    assert weather is None


@patch("backend.services.weather_service.requests.get")
def test_get_weather_invalid_response(mock_get):
    """Test weather fetch with invalid response."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"invalid": "data"}
    mock_get.return_value = mock_response

    weather = WeatherService.get_weather(40.7128, -74.0060)

    assert weather is None


def test_get_weather_description():
    """Test weather description mapping."""
    assert WeatherService.get_weather_description(0) == "Clear sky"
    assert WeatherService.get_weather_description(61) == "Slight rain"
    assert WeatherService.get_weather_description(95) == "Thunderstorm"
    assert WeatherService.get_weather_description(999) == "Unknown"


@pytest.mark.integration
def test_get_weather_real_api():
    """Test weather fetch with real API (integration test)."""
    # Test with New York coordinates
    weather = WeatherService.get_weather(40.7128, -74.0060)

    # API might be unavailable or blocked, so we accept None
    if weather is not None:
        assert "temperature" in weather
        assert "windspeed" in weather
        assert "latitude" in weather
        assert "longitude" in weather
        assert weather["latitude"] == 40.7128
        assert weather["longitude"] == -74.006
        assert isinstance(weather["temperature"], (int, float))


@pytest.mark.integration
def test_get_weather_description_all_codes():
    """Test all weather description codes."""
    # Test all documented codes
    codes = {
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

    for code, description in codes.items():
        assert WeatherService.get_weather_description(code) == description


@patch("backend.services.weather_service.requests.get")
def test_get_weather_timeout(mock_get):
    """Test weather fetch with timeout."""
    mock_get.side_effect = requests.exceptions.Timeout("Request timed out")

    weather = WeatherService.get_weather(40.7128, -74.0060)

    assert weather is None


@patch("backend.services.weather_service.requests.get")
def test_get_weather_http_error(mock_get):
    """Test weather fetch with HTTP error."""
    mock_get.side_effect = requests.exceptions.HTTPError("404 Not Found")

    weather = WeatherService.get_weather(40.7128, -74.0060)

    assert weather is None


@patch("backend.services.weather_service.requests.get")
def test_get_weather_missing_temperature(mock_get):
    """Test weather fetch with missing temperature field."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "current_weather": {
            "windspeed": 15.0,
            "winddirection": 180,
            "weathercode": 0,
            "time": "2025-10-27T14:00",
        }
    }
    mock_get.return_value = mock_response

    weather = WeatherService.get_weather(40.7128, -74.0060)

    # Should still return data with None for temperature
    assert weather is not None
    assert weather["temperature"] is None
