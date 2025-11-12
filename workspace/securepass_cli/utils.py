# Utility functions for SecurePass CLI

from datetime import datetime


def current_utc_isoformat() -> str:
    """Return the current UTC time as an ISO formatted string."""
    return datetime.utcnow().isoformat() + 'Z'
