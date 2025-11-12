from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.models.url_mapping import URLCreate, URLInfo, URLMapping
from app.services.url_service.py import URLService
from app.db.database import get_db
from typing import List
from app.auth.auth import api_key_auth

router = APIRouter(
    prefix="",
    tags=["url_shortener"],
    dependencies=[Depends(api_key_auth)]  # Protect endpoints with API key
)

@router.post("/urls", response_model=URLInfo, status_code=status.HTTP_201_CREATED)
def create_short_url(url_create: URLCreate, db: Session = Depends(get_db)):
    service = URLService(db)
    try:
        url_mapping = service.create_short_url(url_create)
    except HTTPException as e:
        raise e
    return URLInfo(
        short_url=f"https://short.ly/{url_mapping.short_code}",
        long_url=url_mapping.long_url,
        clicks=url_mapping.click_count,
        created_at=url_mapping.created_at,
        expiration_date=url_mapping.expiration_date
    )

@router.get("/urls", response_model=dict)
def list_short_urls(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    service = URLService(db)
    urls = service.list_urls(limit=limit, offset=offset)
    total = len(urls)  # For demo, normally count total in DB
    urls_out = [
        URLInfo(
            short_url=f"https://short.ly/{url.short_code}",
            long_url=url.long_url,
            clicks=url.click_count,
            created_at=url.created_at,
            expiration_date=url.expiration_date
        ) for url in urls
    ]
    return {"urls": urls_out, "total": total}

@router.get("/{short_code}", include_in_schema=False)
def redirect_short_url(short_code: str, db: Session = Depends(get_db)):
    service = URLService(db)
    url_mapping = service.get_url_by_code(short_code)
    if not url_mapping:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")
    # Check expiration
    if url_mapping.expiration_date and url_mapping.expiration_date < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="URL expired")
    # Increment click count
    service.increment_click_count(url_mapping)
    return RedirectResponse(url=url_mapping.long_url)
