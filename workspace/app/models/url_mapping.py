from sqlalchemy import Column, Integer, String, DateTime, func, UniqueConstraint
from app.db.database import Base
from pydantic import BaseModel, HttpUrl, validator
from datetime import datetime, date
from typing import Optional

class URLMapping(Base):
    __tablename__ = 'url_mappings'
    id = Column(Integer, primary_key=True, index=True)
    long_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expiration_date = Column(DateTime(timezone=True), nullable=True)
    click_count = Column(Integer, default=0, nullable=False)
    owner_id = Column(String, nullable=True)  # For future use if needed

    __table_args__ = (
        UniqueConstraint('short_code', name='uq_short_code'),
    )

# Pydantic Schemas

class URLCreate(BaseModel):
    long_url: HttpUrl
    custom_alias: Optional[str] = None
    expiration_date: Optional[date] = None

    @validator('custom_alias')
    def validate_custom_alias(cls, v):
        if v:
            if not v.isalnum():
                raise ValueError('custom_alias must be alphanumeric')
            if len(v) < 4 or len(v) > 20:
                raise ValueError('custom_alias length must be between 4 and 20 characters')
        return v

    @validator('expiration_date')
    def validate_expiration_date(cls, v):
        if v and v < date.today():
            raise ValueError('expiration_date cannot be in the past')
        return v

class URLInfo(BaseModel):
    short_url: str
    long_url: str
    clicks: int
    created_at: datetime
    expiration_date: Optional[datetime]

    class Config:
        orm_mode = True
