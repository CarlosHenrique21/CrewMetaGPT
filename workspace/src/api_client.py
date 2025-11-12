import requests
from datetime import datetime
from src.config import Config
from src.models import WeatherData, DailyForecast

class WeatherAPIClient:
    """Client to interact with the OpenWeatherMap API."""

    def __init__(self, api_key=None, base_url=None, units=None):
        self.api_key = api_key or Config.get_api_key()
        self.base_url = base_url or Config.get_base_url()
        self.units = units or Config.get_default_units()

    def fetch_current_weather(self, location_query):
        """Fetch current weather for a given location (city name or coordinates)."""
        url = f"{self.base_url}weather"
        params = {
            "appid": self.api_key,
            "units": self.units
        }
        # Determine if location_query is city name or coordinates
        if isinstance(location_query, str):
            params["q"] = location_query
        elif isinstance(location_query, dict):
            lat = location_query.get("lat")
            lon = location_query.get("lon")
            if lat is None or lon is None:
                raise ValueError("Coordinates dictionary must contain 'lat' and 'lon'.")
            params["lat"] = lat
            params["lon"] = lon
        else:
            raise ValueError("location_query must be string city name or dict with lat/lon.")

        response = requests.get(url, params=params, timeout=5)

        if response.status_code != 200:
            raise RuntimeError(f"API error: {response.status_code} - {response.text}")

        data = response.json()

        return self._parse_current_weather(data)

    def fetch_forecast(self, location_query, days=5):
        """Fetch forecast for a given location. OpenWeatherMap offers 5-day forecast every 3 hours.
        We will summarize per day."""
        url = f"{self.base_url}forecast"
        params = {
            "appid": self.api_key,
            "units": self.units
        }
        if isinstance(location_query, str):
            params["q"] = location_query
        elif isinstance(location_query, dict):
            lat = location_query.get("lat")
            lon = location_query.get("lon")
            if lat is None or lon is None:
                raise ValueError("Coordinates dictionary must contain 'lat' and 'lon'.")
            params["lat"] = lat
            params["lon"] = lon
        else:
            raise ValueError("location_query must be string city name or dict with lat/lon.")

        response = requests.get(url, params=params, timeout=5)

        if response.status_code != 200:
            raise RuntimeError(f"API error: {response.status_code} - {response.text}")

        data = response.json()

        return self._parse_forecast(data, days)

    def _parse_current_weather(self, data):
        weather_desc = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"].get("speed", 0)
        sunrise_ts = data["sys"].get("sunrise")
        sunset_ts = data["sys"].get("sunset")

        sunrise = datetime.fromtimestamp(sunrise_ts) if sunrise_ts else None
        sunset = datetime.fromtimestamp(sunset_ts) if sunset_ts else None

        return WeatherData(
            temperature=temp,
            humidity=humidity,
            wind_speed=wind_speed,
            condition_description=weather_desc,
            sunrise_time=sunrise,
            sunset_time=sunset
        )

    def _parse_forecast(self, data, days):
        # The forecast data comes in 3-hour chunks. We'll group by days (date) and average the temperature etc.
        day_data = {}

        for entry in data.get("list", []):
            dt_txt = entry["dt_txt"]  # format "YYYY-mm-dd HH:MM:SS"
            date_str = dt_txt.split()[0]

            if date_str not in day_data:
                day_data[date_str] = {
                    "temps": [],
                    "humidities": [],
                    "wind_speeds": [],
                    "conditions": []
                }

            day_data[date_str]["temps"].append(entry["main"]["temp"])
            day_data[date_str]["humidities"].append(entry["main"]["humidity"])
            day_data[date_str]["wind_speeds"].append(entry["wind"]["speed"])
            day_data[date_str]["conditions"].append(entry["weather"][0]["description"].capitalize())

        daily_forecasts = []
        for i, (date_str, vals) in enumerate(sorted(day_data.items())):
            if i >= days:
                break
            temp_avg = sum(vals["temps"]) / len(vals["temps"])
            humidity_avg = int(sum(vals["humidities"]) / len(vals["humidities"]))
            wind_avg = sum(vals["wind_speeds"]) / len(vals["wind_speeds"])
            # Pick most frequent condition
            condition = max(set(vals["conditions"]), key=vals["conditions"].count)

            forecast = DailyForecast(
                date=datetime.strptime(date_str, "%Y-%m-%d"),
                temperature=temp_avg,
                humidity=humidity_avg,
                wind_speed=wind_avg,
                condition_description=condition
            )
            daily_forecasts.append(forecast)

        return daily_forecasts
