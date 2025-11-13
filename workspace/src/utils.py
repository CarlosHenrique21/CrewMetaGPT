"""
Utility functions and constants for SecurePass CLI Generator.
"""

import string

# Character sets
LOWERCASE_LETTERS = string.ascii_lowercase
UPPERCASE_LETTERS = string.ascii_uppercase
DIGITS = string.digits
SPECIAL_CHARACTERS = "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?`~"

# Allowed strengths
ALLOWED_STRENGTHS = {'weak', 'medium', 'strong'}


def validate_length(length: int) -> bool:
    """Validate that password length is between 8 and 64."""
    return 8 <= length <= 64


def validate_strength(strength: str) -> bool:
    """Check if strength is one of the allowed levels."""
    return strength in ALLOWED_STRENGTHS
