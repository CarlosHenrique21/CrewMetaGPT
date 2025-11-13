import unittest
from storage import Storage

class TestStorage(unittest.TestCase):
    def setUp(self):
        self.storage = Storage('test_data.json')

    def test_set_and_get(self):
        self.storage.set('key1', 'value1')
        self.assertEqual(self.storage.get('key1'), 'value1')

    def test_load_data(self):
        self.storage.set('key2', 'value2')
        new_storage = Storage('test_data.json')
        self.assertEqual(new_storage.get('key2'), 'value2')

if __name__ == '__main__':
    unittest.main()