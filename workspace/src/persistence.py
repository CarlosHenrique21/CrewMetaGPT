import json
import os
import tempfile
from typing import List
from src.models import Task

TASKS_FILE = os.path.join(os.path.expanduser('~'), '.cli_task_manager_tasks.json')


def load_tasks() -> List[Task]:
    """Load tasks from the JSON file, return list of Task objects."""
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        tasks = []
        for item in data:
            # Create Task object from dictionary, handling optional fields
            task = Task(
                id=item['id'],
                description=item['description'],
                status=item.get('status', 'pending'),
                priority=item.get('priority'),
                due_date=item.get('due_date'),
                created_at=item.get('created_at'),
                updated_at=item.get('updated_at')
            )
            tasks.append(task)
        return tasks
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading tasks file: {e}")
        return []


def save_tasks(tasks: List[Task]) -> None:
    """Save list of Task objects to the JSON file atomically."""
    tmp_fd, tmp_path = tempfile.mkstemp(prefix='tasks_', suffix='.json', dir=os.path.dirname(TASKS_FILE))
    try:
        with os.fdopen(tmp_fd, 'w', encoding='utf-8') as tmp_file:
            json.dump([task.__dict__ for task in tasks], tmp_file, indent=2)
        os.replace(tmp_path, TASKS_FILE)  # atomic replace
    except Exception as e:
        print(f"Error saving tasks file: {e}")
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
