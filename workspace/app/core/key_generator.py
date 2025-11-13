import secrets
import string

BASE62 = string.ascii_letters + string.digits


def generate_short_key(length: int = 6) -> str:
    """Generate a random base62 encoded string of fixed length."""
    return ''.join(secrets.choice(BASE62) for _ in range(length))
