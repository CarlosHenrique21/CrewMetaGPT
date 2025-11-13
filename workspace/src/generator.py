"""
Password generation logic for SecurePass CLI Generator.
"""

import secrets
from typing import List
from src.utils import LOWERCASE_LETTERS, UPPERCASE_LETTERS, DIGITS, SPECIAL_CHARACTERS


def generate_password(length: int, strength: str, include_special: bool) -> str:
    """
    Generate a secure random password.

    Args:
        length (int): Length of the password (8-64).
        strength (str): Password strength: 'weak', 'medium', or 'strong'.
        include_special (bool): Whether to include special characters.

    Returns:
        str: The generated password.
    """
    if length < 8:
        raise ValueError("Password length must be at least 8.")
    if length > 64:
        raise ValueError("Password length cannot exceed 64.")
    if strength not in ('weak', 'medium', 'strong'):
        raise ValueError("Invalid strength value.")

    # Define character pools based on strength
    if strength == 'weak':
        char_pool = LOWERCASE_LETTERS
        if include_special:
            char_pool += SPECIAL_CHARACTERS
    elif strength == 'medium':
        char_pool = LOWERCASE_LETTERS + UPPERCASE_LETTERS + DIGITS
        if include_special:
            char_pool += SPECIAL_CHARACTERS
    else:  # strong
        char_pool = LOWERCASE_LETTERS + UPPERCASE_LETTERS + DIGITS + SPECIAL_CHARACTERS

    if not char_pool:
        raise ValueError("Character pool is empty. Cannot generate password.")

    # Use the secrets module for cryptographically secure random choices
    password = ''.join(secrets.choice(char_pool) for _ in range(length))

    return password


def generate_multiple_passwords(count: int, length: int, strength: str, include_special: bool) -> List[str]:
    """
    Generate multiple secure random passwords.

    Args:
        count (int): Number of passwords to generate.
        length (int): Length of each password.
        strength (str): Strength level.
        include_special (bool): Include special characters or not.

    Returns:
        List[str]: List of generated passwords.
    """
    if count < 1:
        raise ValueError("Count must be at least 1.")

    passwords = []
    for _ in range(count):
        pwd = generate_password(length, strength, include_special)
        passwords.append(pwd)
    return passwords
