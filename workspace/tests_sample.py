import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
import os

from src.api_client import WeatherAPIClient
from src.utils import colorize_condition
from src.config import Config

# Config Tests

def test_get_api_key_success(monkeypatch):
    monkeypatch.setenv('WEATHER_API_KEY', 'test_key')
    Config.API_KEY = ''  # reset cached
    assert Config.get_api_key() == 'test_key'


def test_get_api_key_missing(monkeypatch):
    monkeypatch.delenv('WEATHER_API_KEY', raising=False)
    Config.API_KEY = ''  # reset cached
    with pytest.raises(ValueError) as excinfo:
        Config.get_api_key()
    assert 'API key not set' in str(excinfo.value)

# API Client Tests

@patch('src.api_client.requests.get')
def test_fetch_current_weather_city_success(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "weather": [{"description": "clear sky"}],
        "main": {"temp": 15, "humidity": 40},
        "wind": {"speed": 2.5},
        "sys": {"sunrise": 1600000000, "sunset": 1600040000}
    }
    mock_get.return_value = mock_resp

    client = WeatherAPIClient(api_key="dummy")
    weather = client.fetch_current_weather("London")

    assert weather.temperature == 15
    assert weather.humidity == 40
    assert weather.wind_speed == 2.5
    assert weather.condition_description == "Clear sky"
    assert weather.sunrise_time is not None
    assert weather.sunset_time is not None

@patch('src.api_client.requests.get')
def test_fetch_current_weather_invalid_location_type(mock_get):
    client = WeatherAPIClient(api_key="dummy")
    with pytest.raises(ValueError):
        client.fetch_current_weather([51.5, -0.12])

@patch('src.api_client.requests.get')
def test_fetch_forecast_days_limit(mock_get):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "list": [
            {
                "dt_txt": "2024-06-01 09:00:00",
                "main": {"temp": 20, "humidity": 55},
                "wind": {"speed": 3},
                "weather": [{"description": "light rain"}]
            },
            {
                "dt_txt": "2024-06-02 09:00:00",
                "main": {"temp": 22, "humidity": 60},
                "wind": {"speed": 4},
                "weather": [{"description": "cloudy"}]
            },
            {
                "dt_txt": "2024-06-03 09:00:00",
                "main": {"temp": 19, "humidity": 50},
                "wind": {"speed": 2},
                "weather": [{"description": "clear sky"}]
            }
        ]
    }
    mock_get.return_value = mock_resp

    client = WeatherAPIClient(api_key="dummy")
    forecast = client.fetch_forecast("City", days=2)
    assert len(forecast) == 2
    assert forecast[0].temperature == 20
    assert forecast[1].temperature == 22

# Utils Tests

def test_colorize_condition_known():
    text_obj = colorize_condition("Clear sky")
    assert "yellow" in str(text_obj.style)

    text_obj = colorize_condition("Rain")
    assert "blue" in str(text_obj.style)


def test_colorize_condition_unknown():
    text_obj = colorize_condition("Hurricane")
    assert text_obj.style is None

