import unittest
from weather_service import WeatherService

class TestWeatherService(unittest.TestCase):
    def setUp(self):
        self.service = WeatherService()

    def test_get_current_weather(self):
        weather = self.service.get_current_weather("London")
        self.assertIsNotNone(weather)
        self.assertEqual(weather.location, "London")

if __name__ == "__main__":
    unittest.main()
