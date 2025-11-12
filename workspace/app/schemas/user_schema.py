from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from uuid import UUID
from datetime import datetime

class UserBase(BaseModel):
    username: constr(min_length=3, max_length=100)
    email: Optional[EmailStr] = None

class UserCreate(UserBase):
    password: constr(min_length=6)

class UserResponse(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
