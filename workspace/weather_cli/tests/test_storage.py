import unittest
from storage import Storage

class TestStorage(unittest.TestCase):
    def test_write_and_read_file(self):
        data = {"locations": ["Paris", "Berlin"]}
        Storage.write_file("test_data.json", data)
        
        read_data = Storage.read_file("test_data.json")
        self.assertEqual(read_data, data)

if __name__ == "__main__":
    unittest.main()
