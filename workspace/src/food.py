"""
Food entity module.
Manages food spawning and position.
"""
import random
from src.config import GRID_WIDTH, GRID_HEIGHT

class Food:
    def __init__(self, snake_positions):
        """
        Initialize food with random position not colliding with snake.
        """
        self.position = None
        self.spawn(snake_positions)

    def spawn(self, snake_positions):
        """
        Spawn food in a random free position (not occupied by snake).
        """
        available_positions = [
            (x, y)
            for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT)
            if (x, y) not in snake_positions
        ]

        if not available_positions:
            # No free space; unlikely but handle gracefully
            self.position = None
            return

        self.position = random.choice(available_positions)
