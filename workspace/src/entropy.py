"""
Entropy estimation for passwords (optional module).
"""

import math

def estimate_entropy(password: str) -> float:
    """
    Estimate entropy of a password in bits.

    Args:
        password (str): Password string.

    Returns:
        float: Estimated entropy in bits.

    This is a simplified entropy estimation based on pool size and length.
    """
    if not password:
        return 0.0

    # Determine character pools used
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    pool_size = 0
    if has_lower:
        pool_size += 26
    if has_upper:
        pool_size += 26
    if has_digit:
        pool_size += 10
    if has_special:
        pool_size += 32  # Approximation for typical special chars

    if pool_size == 0:
        return 0.0

    entropy = len(password) * math.log2(pool_size)
    return entropy
