"""
CLI Interface Module

Handles game initialization, user input processing, and terminal display output.
"""

import pygame
from pygame.locals import QUIT, KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_r, K_q
from game_engine import GameEngine
from renderer import Renderer

class CLIInterface:
    def __init__(self):
        self.board_width = 20
        self.board_height = 15
        self.game_engine = GameEngine(self.board_width, self.board_height)
        self.renderer = Renderer(self.board_width, self.board_height)
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 10  # Default speed, can be varied for difficulty

    def process_input(self, event):
        """Process Pygame keyboard input events."""
        if event.type == QUIT:
            self.running = False

        elif event.type == KEYDOWN:
            if event.key == K_UP:
                self.game_engine.change_direction((0, -1))
            elif event.key == K_DOWN:
                self.game_engine.change_direction((0, 1))
            elif event.key == K_LEFT:
                self.game_engine.change_direction((-1, 0))
            elif event.key == K_RIGHT:
                self.game_engine.change_direction((1, 0))
            elif event.key == K_r and self.game_engine.is_game_over():
                self.game_engine.reset()
            elif event.key == K_q and self.game_engine.is_game_over():
                self.running = False

    def run(self):
        """Main loop to run the game."""
        while self.running:
            for event in pygame.event.get():
                self.process_input(event)

            if not self.game_engine.is_game_over():
                self.game_engine.update()

            self.renderer.render(
                self.game_engine.get_snake_positions(),
                self.game_engine.get_food_position(),
                self.game_engine.get_score(),
                self.game_engine.is_game_over()
            )

            self.clock.tick(self.fps)

        self.renderer.quit()
