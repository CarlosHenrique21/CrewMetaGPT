from typing import Optional
from secrets import choice
from .config import (StrengthLevel, CHARACTER_SETS, MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH)
from .security import secure_random_choice

class PasswordGenerator:
    def __init__(self):
        pass

    def generate_password(self, length: int, include_special_chars: bool, strength: StrengthLevel, seed: Optional[int] = None) -> str:
        """
        Generate a password based on length, inclusion of special characters and strength level.
        Args:
            length (int): Length of the password
            include_special_chars (bool): Whether to include special characters
            strength (StrengthLevel): Strength level of password
            seed (Optional[int]): Seed for repeatability (not implemented for security reasons)

        Returns:
            str: Generated password
        """
        # Input validation
        if length < MIN_PASSWORD_LENGTH or length > MAX_PASSWORD_LENGTH:
            raise ValueError(f"Password length must be between {MIN_PASSWORD_LENGTH} and {MAX_PASSWORD_LENGTH}")

        # Select base character set based on strength
        char_set = CHARACTER_SETS[strength]

        if include_special_chars:
            # For weak and moderate, add special characters if specified
            if strength != StrengthLevel.STRONG:
                # Add special characters to the char set if not already included
                char_set += ''.join(c for c in CHARACTER_SETS[StrengthLevel.STRONG] if c not in char_set)

        # Removal of duplicate characters
        char_set = ''.join(sorted(set(char_set)))

        if not char_set:
            raise ValueError("Character set for password generation is empty.")

        # Generate password using cryptographically secure random selection
        password_chars = [secure_random_choice(char_set) for _ in range(length)]

        password = ''.join(password_chars)

        return password
