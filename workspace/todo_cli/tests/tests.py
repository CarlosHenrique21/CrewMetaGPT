import unittest
from todo_cli.task_manager import TaskManager
from todo_cli.models import Task

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.task_manager = TaskManager(storage_file='test_tasks.json')
        self.task_manager.tasks = []  # Clear existing tasks for testing

    def test_add_task(self):
        self.task_manager.add_task("Test Task", "Test Description")
        self.assertEqual(len(self.task_manager.tasks), 1)
        self.assertEqual(self.task_manager.tasks[0].title, "Test Task")

    def test_list_tasks(self):
        self.task_manager.add_task("Task 1", "Description 1")
        self.task_manager.add_task("Task 2", "Description 2")
        tasks = self.task_manager.list_tasks()
        self.assertEqual(len(tasks), 2)

    def test_mark_done(self):
        self.task_manager.add_task("Task 1", "Description 1")
        self.task_manager.mark_done(1)
        self.assertTrue(self.task_manager.tasks[0].completed)

    def test_delete_task(self):
        self.task_manager.add_task("Task 1", "Description 1")
        self.task_manager.delete_task(1)
        self.assertEqual(len(self.task_manager.tasks), 0)

    def tearDown(self):
        import os
        os.remove('test_tasks.json')  # Clean up test file

if __name__ == '__main__':
    unittest.main()