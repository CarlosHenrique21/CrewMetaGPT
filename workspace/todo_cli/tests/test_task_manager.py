# test_task_manager.py

import unittest
from task_manager import TaskManager
from models import Task

class TestTaskManager(unittest.TestCase):
    
    def setUp(self):
        """Set up a temporary task manager for testing."""
        self.manager = TaskManager(storage_file='test_tasks.json')

    def test_add_task(self):
        """Test adding a task."""
        self.manager.add_task(title="Test Task")
        tasks = self.manager.list_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Test Task")

    def test_mark_done(self):
        """Test marking a task as done."""
        self.manager.add_task(title="Test Task")
        self.manager.mark_done(1)
        tasks = self.manager.list_tasks()
        self.assertTrue(tasks[0].completed)

    def test_delete_task(self):
        """Test deleting a task."""
        self.manager.add_task(title="Test Task")
        self.manager.delete_task(1)
        tasks = self.manager.list_tasks()
        self.assertEqual(len(tasks), 0)

if __name__ == '__main__':
    unittest.main()
