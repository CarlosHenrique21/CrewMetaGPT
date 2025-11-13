from typing import List, Optional
from datetime import datetime
from src.models import Task, TaskStatus
from src.persistence import load_tasks, save_tasks

class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []
        self.load_tasks()

    def load_tasks(self):
        self.tasks = load_tasks()

    def save_tasks(self):
        save_tasks(self.tasks)

    def _generate_next_id(self) -> int:
        if not self.tasks:
            return 1
        return max(task.id for task in self.tasks) + 1

    def add_task(self, description: str, priority: Optional[int] = None, due_date: Optional[str] = None) -> Task:
        """Add a new task with description, optional priority and due_date."""
        task_id = self._generate_next_id()
        new_task = Task(
            id=task_id,
            description=description,
            priority=priority,
            due_date=due_date,
            status=TaskStatus.PENDING
        )
        self.tasks.append(new_task)
        self.save_tasks()
        return new_task

    def list_tasks(self, status_filter: Optional[str] = None) -> List[Task]:
        """Return list of tasks filtered by status (pending/done/all)."""
        if status_filter is None or status_filter.lower() == 'all':
            return self.tasks
        filtered = []
        try:
            status_enum = TaskStatus(status_filter.lower())
        except ValueError:
            # Invalid status filter; return empty list
            return []
        for task in self.tasks:
            if task.status == status_enum:
                filtered.append(task)
        return filtered

    def mark_done(self, task_id: int) -> bool:
        """Mark task as done by id. Returns True if successful."""
        for task in self.tasks:
            if task.id == task_id:
                if task.status == TaskStatus.DONE:
                    return False  # Already done
                task.mark_done()
                self.save_tasks()
                return True
        return False  # Not found

    def delete_task(self, task_id: int) -> bool:
        """Delete task by id. Returns True if deleted."""
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                self.tasks.pop(i)
                self.save_tasks()
                return True
        return False
