from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

class TaskStatus(str, Enum):
    PENDING = "pending"
    DONE = "done"

@dataclass
class Task:
    id: int
    description: str
    status: TaskStatus = TaskStatus.PENDING
    priority: Optional[int] = None
    due_date: Optional[str] = None  # ISO8601 date string (YYYY-MM-DD)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + 'Z')
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + 'Z')

    def mark_done(self):
        """Mark the task as done and update the timestamp."""
        self.status = TaskStatus.DONE
        self.updated_at = datetime.utcnow().isoformat() + 'Z'

    def update_description(self, new_description: str):
        """Update the description of the task."""
        self.description = new_description
        self.updated_at = datetime.utcnow().isoformat() + 'Z'
