"""
Game module.
Contains the Game class which manages game state, updates, and main logic.
"""
import pygame
from src.snake import Snake
from src.food import Food
from src.score import Score
from src.config import GRID_WIDTH, GRID_HEIGHT

class Game:
    def __init__(self):
        initial_snake_pos = [(GRID_WIDTH // 2, GRID_HEIGHT // 2), (GRID_WIDTH // 2 -1, GRID_HEIGHT // 2), (GRID_WIDTH // 2 -2, GRID_HEIGHT // 2)]
        self.snake = Snake(initial_snake_pos)
        self.food = Food(self.snake.positions)
        self.score = Score()
        self.game_over = False

    def reset(self):
        """Reset the game to initial state."""
        initial_snake_pos = [(GRID_WIDTH // 2, GRID_HEIGHT // 2), (GRID_WIDTH // 2 -1, GRID_HEIGHT // 2), (GRID_WIDTH // 2 -2, GRID_HEIGHT // 2)]
        self.snake = Snake(initial_snake_pos)
        self.food.spawn(self.snake.positions)
        self.score.reset()
        self.game_over = False

    def update(self, direction):
        """
        Update game state: move snake, check collisions, update score.

        direction: tuple (dx, dy) or None
        """
        if self.game_over:
            return

        if direction:
            self.snake.turn(direction)

        self.snake.move()

        head = self.snake.get_head_position()

        # Check boundary collision
        if not (0 <= head[0] < GRID_WIDTH and 0 <= head[1] < GRID_HEIGHT):
            self.game_over = True
            self.score.save_high_score()
            return

        # Check self collision
        if self.snake.check_self_collision():
            self.game_over = True
            self.score.save_high_score()
            return

        # Check food collision
        if head == self.food.position:
            self.snake.grow()
            self.score.increase(1)
            self.food.spawn(self.snake.positions)

    def is_game_over(self):
        return self.game_over

    def get_snake_positions(self):
        return self.snake.positions

    def get_food_position(self):
        return self.food.position

    def get_score(self):
        return self.score.current_score

    def get_high_score(self):
        return self.score.high_score
