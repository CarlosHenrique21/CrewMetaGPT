# task_manager.py

import json
from models import Task
from typing import List, Optional

class TaskManager:
    def __init__(self, storage_file: str = 'tasks.json'):
        self.storage_file = storage_file
        self.tasks: List[Task] = self.load_tasks()

    def load_tasks(self) -> List[Task]:
        """Load tasks from the JSON file."""
        try:
            with open(self.storage_file, 'r') as file:
                tasks_data = json.load(file)
                return [Task(**task) for task in tasks_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self) -> None:
        """Save tasks to the JSON file."""
        with open(self.storage_file, 'w') as file:
            json.dump([task.__dict__ for task in self.tasks], file, default=str)

    def add_task(self, title: str, description: Optional[str] = "") -> None:
        """Add a new task."""
        task_id = len(self.tasks) + 1  # Simple ID generation
        new_task = Task(id=task_id, title=title, description=description)
        self.tasks.append(new_task)
        self.save_tasks()

    def list_tasks(self) -> List[Task]:
        """Return a list of tasks."""
        return self.tasks

    def mark_done(self, task_id: int) -> None:
        """Mark a task as done."""
        for task in self.tasks:
            if task.id == task_id:
                task.completed = True
                self.save_tasks()
                return
        print("Task not found.")

    def delete_task(self, task_id: int) -> None:
        """Delete a task by ID."""
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.save_tasks()
