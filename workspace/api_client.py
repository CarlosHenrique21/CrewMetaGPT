import requests
from config import Config
from errors import APIRequestError


BASE_URL = 'https://api.openweathermap.org/data/2.5'


def get_current_weather(location, unit='celsius'):
    """
    Fetch current weather for location.
    Location can be city name (str) or coordinates (tuple of lat, lon).
    Unit can be 'celsius' or 'fahrenheit'.
    Returns dict with weather data.
    Raises APIRequestError on failure.
    """
    api_key = Config().api_key
    if not api_key:
        raise APIRequestError('API key not configured. Please set it in config.json')

    params = {'appid': api_key}

    # Prepare location query
    if isinstance(location, str):
        params['q'] = location
    elif isinstance(location, (tuple, list)) and len(location) == 2:
        params['lat'] = location[0]
        params['lon'] = location[1]
    else:
        raise APIRequestError('Invalid location format')

    # Units setting
    if unit == 'celsius':
        params['units'] = 'metric'
    elif unit == 'fahrenheit':
        params['units'] = 'imperial'
    else:
        params['units'] = 'standard'

    url = f'{BASE_URL}/weather'
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data.get('cod') != 200:
            raise APIRequestError(f"API error: {data.get('message', '')}")

        return data
    except requests.RequestException as e:
        raise APIRequestError(f'Network error: {str(e)}')


def get_forecast(location, days=3, unit='celsius'):
    """
    Fetch weather forecast for the next 'days' days.
    Location same format as get_current_weather.
    Returns dict with forecast data.
    Raises APIRequestError on failure.
    """
    api_key = Config().api_key
    if not api_key:
        raise APIRequestError('API key not configured. Please set it in config.json')

    params = {'appid': api_key}

    # Prepare location query
    if isinstance(location, str):
        params['q'] = location
    elif isinstance(location, (tuple, list)) and len(location) == 2:
        params['lat'] = location[0]
        params['lon'] = location[1]
    else:
        raise APIRequestError('Invalid location format')

    # Units setting
    if unit == 'celsius':
        params['units'] = 'metric'
    elif unit == 'fahrenheit':
        params['units'] = 'imperial'
    else:
        params['units'] = 'standard'

    params['cnt'] = days * 8  # OpenWeatherMap provides 3-hour intervals, 8 per day

    url = f'{BASE_URL}/forecast'
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        if data.get('cod') not in ('200', 200):
            raise APIRequestError(f"API error: {data.get('message', '')}")

        return data
    except requests.RequestException as e:
        raise APIRequestError(f'Network error: {str(e)}')
