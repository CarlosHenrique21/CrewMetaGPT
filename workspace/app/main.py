from fastapi import FastAPI
from app.api import endpoints
from app.db.database import engine, Base

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener API")

app.include_router(endpoints.router)

@app.get("/healthz", tags=["health"])
def health_check():
    return {"status": "ok"}
