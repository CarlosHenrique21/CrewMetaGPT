import asyncio
from typing import List, Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.url_mapping import URLMapping
from app.core.key_generator import generate_short_key
from app.core.config import settings
from fastapi import HTTPException, status


class URLService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_short_url(self, long_url: str, custom_alias: Optional[str] = None) -> URLMapping:
        # Check for existing custom alias
        if custom_alias:
            existing = await self._get_by_short_key(custom_alias)
            if existing:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Custom alias already in use")
            short_key = custom_alias
        else:
            # Generate unique short key
            short_key = await self._generate_unique_short_key()

        url_mapping = URLMapping(short_key=short_key, long_url=long_url)
        self.db.add(url_mapping)
        await self.db.commit()
        await self.db.refresh(url_mapping)
        return url_mapping

    async def _generate_unique_short_key(self) -> str:
        # Generate short key and verify uniqueness
        for _ in range(5):  # Retry max 5 times
            short_key = generate_short_key()
            exists = await self._get_by_short_key(short_key)
            if not exists:
                return short_key
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not generate unique short URL key")

    async def _get_by_short_key(self, short_key: str) -> Optional[URLMapping]:
        result = await self.db.execute(select(URLMapping).where(
            (URLMapping.short_key == short_key) | (URLMapping.custom_alias == short_key))
        )
        return result.scalar_one_or_none()

    async def list_urls(self) -> List[URLMapping]:
        result = await self.db.execute(select(URLMapping))
        return result.scalars().all()

    async def get_long_url(self, short_key: str) -> URLMapping:
        url_mapping = await self._get_by_short_key(short_key)
        if not url_mapping:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found")
        return url_mapping

    async def increment_click_count(self, url_mapping: URLMapping) -> None:
        # Increment click_count asynchronously
        await self.db.execute(
            update(URLMapping)
            .where(URLMapping.id == url_mapping.id)
            .values(click_count=URLMapping.click_count + 1)
        )
        await self.db.commit()
