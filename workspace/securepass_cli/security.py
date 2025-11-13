import secrets
import string

# Security utilities

def secure_random_choice(seq: str) -> str:
    """Select a cryptographically secure random character from the sequence."""
    return secrets.choice(seq)


def secure_random_seed(seed: int):
    """
    For future extension - set seed if needed.
    Note: Python secrets module does not support seed. Using random for seed is not secure.
    """
    # Intentionally left blank to enforce using secrets module for security
    pass
