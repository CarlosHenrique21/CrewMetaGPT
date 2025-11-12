import os

class Config:
    """Configuration management for the CLI Weather Forecast Tool."""

    API_KEY = os.getenv("WEATHER_API_KEY", "")  # User must set this environment variable
    BASE_URL = "https://api.openweathermap.org/data/2.5/"
    DEFAULT_UNITS = "metric"  # 'metric' or 'imperial'

    @classmethod
    def get_api_key(cls):
        if not cls.API_KEY:
            raise ValueError("API key not set. Please set the WEATHER_API_KEY environment variable.")
        return cls.API_KEY

    @classmethod
    def get_base_url(cls):
        return cls.BASE_URL

    @classmethod
    def get_default_units(cls):
        return cls.DEFAULT_UNITS
