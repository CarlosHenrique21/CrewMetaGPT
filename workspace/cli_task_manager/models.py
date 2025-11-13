from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    id: int
    description: str
    status: str  # 'pending' or 'done'
    priority: Optional[int] = None
    due_date: Optional[datetime] = None
    created_at: datetime = datetime.now()
    completed_at: Optional[datetime] = None
