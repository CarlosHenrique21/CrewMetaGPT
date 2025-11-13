from pydantic import BaseModel, constr, conint
from typing import Optional
from uuid import UUID
from datetime import date, datetime
from enum import Enum

class StatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in-progress"
    done = "done"

class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskBase(BaseModel):
    title: constr(min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[StatusEnum] = StatusEnum.pending
    priority: Optional[PriorityEnum] = PriorityEnum.medium
    due_date: Optional[date] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[constr(min_length=1, max_length=255)] = None
    description: Optional[str] = None
    status: Optional[StatusEnum] = None
    priority: Optional[PriorityEnum] = None
    due_date: Optional[date] = None

class TaskResponse(TaskBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
