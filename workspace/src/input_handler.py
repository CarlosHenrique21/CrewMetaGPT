"""
Input handler module.
Captures keyboard events using Pygame and converts to direction commands for the snake.
"""
import pygame
from src.config import UP, DOWN, LEFT, RIGHT

KEY_DIRECTION_MAP = {
    pygame.K_UP: UP,
    pygame.K_w: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_s: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_a: LEFT,
    pygame.K_RIGHT: RIGHT,
    pygame.K_d: RIGHT
}

class InputHandler:
    def __init__(self):
        self.direction = RIGHT  # Default direction

    def process_events(self):
        """
        Process Pygame events and update direction based on key presses.
        Returns the new direction or None if no change.
        """
        new_direction = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'QUIT'
            elif event.type == pygame.KEYDOWN:
                if event.key in KEY_DIRECTION_MAP:
                    new_direction = KEY_DIRECTION_MAP[event.key]
                elif event.key == pygame.K_ESCAPE:
                    return 'QUIT'
        return new_direction
