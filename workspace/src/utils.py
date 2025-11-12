import random


def get_random_position(width, height, exclude_positions):
    """Generate random position on the grid excluding given positions."""
    while True:
        pos = (random.randint(0, width - 1), random.randint(0, height - 1))
        if pos not in exclude_positions:
            return pos
