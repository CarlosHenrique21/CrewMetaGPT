# test_cli.py

import unittest
import subprocess

class TestCLI(unittest.TestCase):

    def test_add_task(self):
        """Test adding a task via CLI."""
        result = subprocess.run(['python3', 'cli.py', 'add', '--title', 'Test Task'], capture_output=True, text=True)
        self.assertIn("Task added successfully.", result.stdout)

    def test_list_tasks(self):
        """Test listing tasks via CLI."""
        subprocess.run(['python3', 'cli.py', 'add', '--title', 'Test List Task'])
        result = subprocess.run(['python3', 'cli.py', 'list'], capture_output=True, text=True)
        self.assertIn("Test List Task", result.stdout)

if __name__ == '__main__':
    unittest.main()
