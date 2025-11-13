import random
import string
from dataclasses import dataclass

@dataclass
class PasswordCriteria:
    length: int
    include_uppercase: bool
    include_lowercase: bool
    include_numbers: bool
    include_special_chars: bool

class PasswordManager:
    def generate_password(self, criteria: PasswordCriteria) -> str:
        characters = ''
        if criteria.include_uppercase:
            characters += string.ascii_uppercase
        if criteria.include_lowercase:
            characters += string.ascii_lowercase
        if criteria.include_numbers:
            characters += string.digits
        if criteria.include_special_chars:
            characters += string.punctuation

        # Check if characters is empty
        if not characters:
            raise ValueError('At least one character type must be selected.')

        # Generate password
        password = ''.join(random.choice(characters) for _ in range(criteria.length))
        return password