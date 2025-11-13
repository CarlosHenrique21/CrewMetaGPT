import unittest
from cache_manager import CacheManager

class TestCacheManager(unittest.TestCase):
    def setUp(self):
        self.cache = CacheManager()

    def test_cache_set_and_get(self):
        loc = 'TestLocation'
        unit = 'celsius'
        data = {'temp': 20}
        self.cache.set_cache(loc, unit, data)
        cached_data = self.cache.get_cached(loc, unit)
        self.assertEqual(cached_data, data)

    def test_cache_forecast_set_and_get(self):
        loc = 'TestLocation'
        unit = 'celsius'
        data = {'forecast': []}
        days = 3
        self.cache.set_cache_forecast(loc, unit, days, data)
        cached_data = self.cache.get_cached_forecast(loc, unit, days)
        self.assertEqual(cached_data, data)

if __name__ == '__main__':
    unittest.main()
