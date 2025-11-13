# test_storage.py

import unittest
import os
from storage import Storage
from models import Task

class TestStorage(unittest.TestCase):
    
    def setUp(self):
        """Set up a test storage file."""
        self.test_file = 'test_storage.json'
        self.storage = Storage(storage_file=self.test_file)

    def tearDown(self):
        """Remove the test storage file after tests."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_and_load_tasks(self):
        """Test saving and loading tasks."""
        task = Task(id=1, title="Test Task")
        self.storage.save_tasks([task])
        loaded_tasks = self.storage.load_tasks()
        self.assertEqual(len(loaded_tasks), 1)
        self.assertEqual(loaded_tasks[0].title, "Test Task")

if __name__ == '__main__':
    unittest.main()
