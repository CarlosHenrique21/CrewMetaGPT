# storage.py

import json
from models import Task
from typing import List

class Storage:
    def __init__(self, storage_file: str):
        self.storage_file = storage_file

    def load_tasks(self) -> List[Task]:
        """Load tasks from the JSON file."""
        try:
            with open(self.storage_file, 'r') as file:
                tasks_data = json.load(file)
                return [Task(**task) for task in tasks_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self, tasks: List[Task]) -> None:
        """Save tasks to the JSON file."""
        with open(self.storage_file, 'w') as file:
            json.dump([task.__dict__ for task in tasks], file, default=str)
