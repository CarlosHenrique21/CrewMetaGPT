import pygame
from src.constants import UP, DOWN, LEFT, RIGHT

class InputHandler:
    def __init__(self):
        self.current_direction = RIGHT  # Default start moving right

    def get_latest_direction(self):
        """Processes pygame events and updates the current direction.
        Returns the direction as a tuple (dx, dy)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Return None to indicate quit
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.current_direction != DOWN:
                    self.current_direction = UP
                elif event.key == pygame.K_DOWN and self.current_direction != UP:
                    self.current_direction = DOWN
                elif event.key == pygame.K_LEFT and self.current_direction != RIGHT:
                    self.current_direction = LEFT
                elif event.key == pygame.K_RIGHT and self.current_direction != LEFT:
                    self.current_direction = RIGHT
        return self.current_direction
