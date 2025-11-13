import json
from pathlib import Path
from datetime import datetime, timedelta
from errors import CacheError


class CacheManager:
    CACHE_DIR = Path.home() / '.weather-cli'
    CACHE_FILE = CACHE_DIR / 'cache.json'
    FORECAST_CACHE_FILE = CACHE_DIR / 'cache_forecast.json'

    def __init__(self):
        self.CACHE_DIR.mkdir(exist_ok=True, parents=True)
        if not self.CACHE_FILE.exists():
            with open(self.CACHE_FILE, 'w') as f:
                json.dump({}, f)
        if not self.FORECAST_CACHE_FILE.exists():
            with open(self.FORECAST_CACHE_FILE, 'w') as f:
                json.dump({}, f)

    def _load_cache(self, forecast=False):
        file_path = self.FORECAST_CACHE_FILE if forecast else self.CACHE_FILE
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise CacheError(f'Error loading cache file: {str(e)}')

    def _save_cache(self, data, forecast=False):
        file_path = self.FORECAST_CACHE_FILE if forecast else self.CACHE_FILE
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            raise CacheError(f'Error saving cache file: {str(e)}')

    def _make_key(self, location, unit, days=None):
        loc_key = location.replace(' ', '_') if isinstance(location, str) else '_'.join(map(str, location))
        if days:
            return f'{loc_key}_{unit}_forecast_{days}'
        else:
            return f'{loc_key}_{unit}'

    def get_cached(self, location, unit):
        cache = self._load_cache(forecast=False)
        key = self._make_key(location, unit)
        entry = cache.get(key)
        if entry:
            timestamp = datetime.fromisoformat(entry['timestamp'])
            if datetime.now() - timestamp < timedelta(minutes=10):  # cache valid 10 minutes
                return entry['data']
            else:
                # stale cache
                return None
        return None

    def set_cache(self, location, unit, data):
        cache = self._load_cache(forecast=False)
        key = self._make_key(location, unit)
        cache[key] = {
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        self._save_cache(cache, forecast=False)

    def get_cached_forecast(self, location, unit, days):
        cache = self._load_cache(forecast=True)
        key = self._make_key(location, unit, days)
        entry = cache.get(key)
        if entry:
            timestamp = datetime.fromisoformat(entry['timestamp'])
            if datetime.now() - timestamp < timedelta(minutes=60):  # cache forecast valid 60 minutes
                return entry['data']
            else:
                return None
        return None

    def set_cache_forecast(self, location, unit, days, data):
        cache = self._load_cache(forecast=True)
        key = self._make_key(location, unit, days)
        cache[key] = {
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        self._save_cache(cache, forecast=True)
