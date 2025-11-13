from typing import List, Optional
from datetime import datetime
from cli_task_manager.storage import Storage
from cli_task_manager.models import Task

class TaskManagerService:
    def __init__(self):
        self.storage = Storage()

    def add_task(self, description: str, priority: Optional[int] = None, due_date: Optional[str] = None) -> int:
        # Validate description
        description = description.strip()
        if not description:
            raise ValueError("Task description cannot be empty.")

        # Validate due_date format if provided
        if due_date:
            try:
                datetime.strptime(due_date, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Due date must be in YYYY-MM-DD format.")

        task_id = self.storage.add_task(description, priority, due_date)
        return task_id

    def list_tasks(self) -> List[Task]:
        return self.storage.get_tasks()

    def mark_done(self, task_id: int) -> bool:
        if task_id <= 0:
            raise ValueError("Invalid task_id. Must be a positive integer.")
        return self.storage.mark_done(task_id)

    def delete_task(self, task_id: int) -> bool:
        if task_id <= 0:
            raise ValueError("Invalid task_id. Must be a positive integer.")
        return self.storage.delete_task(task_id)

    def close(self):
        self.storage.close()
