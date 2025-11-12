import pytest
from unittest.mock import patch
from src.api_client import WeatherAPIClient

@patch('src.api_client.requests.get')
def test_fetch_current_weather_success(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "weather": [{"description": "clear sky"}],
        "main": {"temp": 20.5, "humidity": 50},
        "wind": {"speed": 3.5},
        "sys": {"sunrise": 1600000000, "sunset": 1600040000}
    }

    client = WeatherAPIClient(api_key="dummy")
    weather = client.fetch_current_weather("London")

    assert weather.temperature == 20.5
    assert weather.humidity == 50
    assert weather.wind_speed == 3.5
    assert weather.condition_description == "Clear sky"
    assert weather.sunrise_time is not None
    assert weather.sunset_time is not None

@patch('src.api_client.requests.get')
def test_fetch_forecast_success(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "list": [
            {
                "dt_txt": "2024-06-01 12:00:00",
                "main": {"temp": 21, "humidity": 60},
                "wind": {"speed": 5},
                "weather": [{"description": "light rain"}]
            },
            {
                "dt_txt": "2024-06-01 15:00:00",
                "main": {"temp": 22, "humidity": 62},
                "wind": {"speed": 4.5},
                "weather": [{"description": "light rain"}]
            }
        ]
    }

    client = WeatherAPIClient(api_key="dummy")
    forecast = client.fetch_forecast("London", days=1)

    assert len(forecast) == 1
    assert forecast[0].temperature == 21.5
    assert forecast[0].humidity == 61
    assert forecast[0].wind_speed == 4.75
    assert forecast[0].condition_description == "Light rain"
