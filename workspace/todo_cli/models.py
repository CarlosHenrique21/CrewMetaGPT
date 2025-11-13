# models.py

from dataclasses import dataclass
from datetime import datetime

dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
