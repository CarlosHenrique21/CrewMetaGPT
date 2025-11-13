import requests
from models import Weather
from datetime import datetime

class WeatherService:
    API_URL = "https://api.weatherapi.com/v1/current.json"  # Example API endpoint
    API_KEY = "YOUR_API_KEY"  # Replace with a secure method to store API keys

    def get_current_weather(self, location: str) -> Weather:
        try:
            response = requests.get(self.API_URL, params={"key": self.API_KEY, "q": location})
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()

            weather = Weather(
                location=data['location']['name'],
                temperature=data['current']['temp_c'],
                humidity=data['current']['humidity'],
                wind_speed=data['current']['wind_kph'],
                forecast=[],  # To be implemented later
                retrieved_at=datetime.now()
            )
            return weather
        except requests.exceptions.RequestException as e:
            return f"Error fetching weather data: {e}"
