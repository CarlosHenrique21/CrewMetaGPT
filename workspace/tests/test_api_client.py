import unittest
from unittest.mock import patch
import api_client


class TestAPIClient(unittest.TestCase):
    @patch('api_client.requests.get')
    def test_get_current_weather_success(self, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = {'cod': 200, 'weather': [{}], 'main': {}, 'wind': {}, 'sys': {}, 'name': 'TestCity'}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = api_client.get_current_weather('TestCity')
        self.assertIn('weather', result)

    @patch('api_client.requests.get')
    def test_get_forecast_success(self, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = {'cod': '200', 'list': [], 'city': {}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = api_client.get_forecast('TestCity')
        self.assertIn('list', result)

if __name__ == '__main__':
    unittest.main()
