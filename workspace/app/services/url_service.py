import string
import random
from sqlalchemy.orm import Session
from app.models.url_mapping import URLMapping, URLCreate
from datetime import datetime
from fastapi import HTTPException, status
from typing import List, Optional

BASE_SHORT_URL = "https://short.ly/"

class URLService:
    def __init__(self, db: Session):
        self.db = db

    def generate_short_code(self, length: int = 6) -> str:
        # Generates a random alphanumeric short code
        chars = string.ascii_letters + string.digits
        while True:
            short_code = ''.join(random.choices(chars, k=length))
            # Check if short_code already exists
            existing = self.db.query(URLMapping).filter(URLMapping.short_code == short_code).first()
            if not existing:
                return short_code

    def create_short_url(self, url_create: URLCreate) -> URLMapping:
        # Check custom alias is unique if provided
        if url_create.custom_alias:
            alias = url_create.custom_alias
            existing = self.db.query(URLMapping).filter(URLMapping.short_code == alias).first()
            if existing:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Custom alias already exists")
            short_code = alias
        else:
            # Generate random short code
            short_code = self.generate_short_code()

        # Convert expiration_date from date to datetime at end of day
        expiration_dt = None
        if url_create.expiration_date:
            expiration_dt = datetime.combine(url_create.expiration_date, datetime.max.time())

        url_mapping = URLMapping(
            long_url=url_create.long_url,
            short_code=short_code,
            expiration_date=expiration_dt
        )

        self.db.add(url_mapping)
        self.db.commit()
        self.db.refresh(url_mapping)
        return url_mapping

    def list_urls(self, limit: int = 10, offset: int = 0) -> List[URLMapping]:
        return self.db.query(URLMapping).order_by(URLMapping.created_at.desc()).offset(offset).limit(limit).all()

    def get_url_by_code(self, short_code: str) -> Optional[URLMapping]:
        return self.db.query(URLMapping).filter(URLMapping.short_code == short_code).first()

    def increment_click_count(self, url_mapping: URLMapping):
        url_mapping.click_count += 1
        self.db.commit()

