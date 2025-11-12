from enum import Enum

class StrengthLevel(Enum):
    WEAK = 'weak'
    MODERATE = 'moderate'
    STRONG = 'strong'

# Default configuration constants
DEFAULT_PASSWORD_LENGTH = 12
MIN_PASSWORD_LENGTH = 4
MAX_PASSWORD_LENGTH = 128

SPECIAL_CHARACTERS = "!@#$%^&*()-_=+[]{}|;:',.<>?/`~"

# Character sets for each strength level
CHARACTER_SETS = {
    StrengthLevel.WEAK: 'abcdefghijklmnopqrstuvwxyz',
    StrengthLevel.MODERATE: 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
    StrengthLevel.STRONG: 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789' + SPECIAL_CHARACTERS
}
