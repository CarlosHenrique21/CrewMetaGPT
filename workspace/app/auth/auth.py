from fastapi import Header, HTTPException, status, Security
from fastapi.security.api_key import APIKeyHeader

API_KEY = "mysecretapikey123"  # In real app, use env or config
API_KEY_NAME = "X-API-KEY"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def api_key_auth(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
            headers={"WWW-Authenticate": "API Key"},
        )
    return api_key
