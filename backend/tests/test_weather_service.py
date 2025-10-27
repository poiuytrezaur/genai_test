"""Unit tests for weather service."""

from unittest.mock import Mock, patch

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
