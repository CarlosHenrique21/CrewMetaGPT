from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.core import security
from app.core.config import settings
from app.core.security import validate_url
from app.models.url_mapping import URLMapping
from app.services.url_service import URLService
from app.core.config import settings
from app.services.url_service import URLService
from app.core.config import settings

from app.core.config import settings
from app.core.security import validate_url


from app.core.config import settings

from app.core.config import settings

from app.core.config import settings

from app.core.config import settings


from app.core.config import settings


from app.core.config import settings


from app.core.config import settings


from app.core.config import settings


from app.core.config import settings


from app.core.config import settings


from app.core.config import settings


from app.core.config import settings


from app.core.config import settings




router = APIRouter()


class URLCreateRequest(BaseModel):
    long_url: HttpUrl
    custom_alias: Optional[str] = None


class URLCreateResponse(BaseModel):
    short_url: str


class URLListItem(BaseModel):
    short_url: str
    long_url: str


@router.post("/urls", response_model=URLCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_short_url(request: URLCreateRequest, db: AsyncSession = Depends()):
    validate_url(str(request.long_url))
    service = URLService(db)
    url_mapping = await service.create_short_url(request.long_url, request.custom_alias)
    short_url = f"{settings.base_url}/{url_mapping.short_key}"
    return URLCreateResponse(short_url=short_url)


@router.get("/urls", response_model=List[URLListItem])
async def list_short_urls(db: AsyncSession = Depends()):
    service = URLService(db)
    url_mappings = await service.list_urls()
    results = [URLListItem(short_url=f"{settings.base_url}/{u.short_key}", long_url=u.long_url) for u in url_mappings]
    return results


@router.get("/{short_key}")
async def redirect_short_url(short_key: str, db: AsyncSession = Depends()):
    service = URLService(db)
    url_mapping = await service.get_long_url(short_key)
    # Increment click count asynchronously without waiting
    # (Fire and forget)
    asyncio.create_task(service.increment_click_count(url_mapping))

    return RedirectResponse(url=url_mapping.long_url)
