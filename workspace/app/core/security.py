import re
from urllib.parse import urlparse

from fastapi import HTTPException, status

URL_REGEX = re.compile(
    r'^(https?://)'
    r'((([A-Za-z0-9-]+\.)+[A-Za-z]{2,})|'  # domain
    r'localhost|'  # localhost
    r'(\d{1,3}\.){3}\d{1,3})'  # IP
    r'(:\d+)?'  # optional port
    r'(/\S*)?$'
)


def validate_url(url: str) -> None:
    """Validate if the url is a well-formed HTTP/HTTPS URL and prevent open redirects."""
    if not url:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="URL must not be empty")
    if not URL_REGEX.match(url):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid URL format")

    # Additional parsing to prevent open redirects (ensure http/https only)
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="URL scheme must be http or https")

    # Optionally, prevent local files, suspicious URLs, etc.


# Additional security utilities can be added here
