import unittest
from location_manager import LocationManager

class TestLocationManager(unittest.TestCase):
    def setUp(self):
        self.manager = LocationManager("test_locations.json")

    def test_save_and_load_location(self):
        self.manager.save_location("New York")
        locations = self.manager.load_locations()
        self.assertIn("New York", locations)

if __name__ == "__main__":
    unittest.main()
