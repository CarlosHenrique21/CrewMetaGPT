"""
Renderer module.
Renders game elements (snake, food, borders, score) using Pygame.
"""
import pygame
from src.config import COLOR_BLACK, COLOR_DARK_GREY, COLOR_RED, COLOR_GREEN, COLOR_WHITE, WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE

class Renderer:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def draw_grid(self):
        """
        Draw grid lines for better visuals.
        """
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, COLOR_DARK_GREY, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, COLOR_DARK_GREY, (0, y), (WINDOW_WIDTH, y))

    def render(self, snake_positions, food_position, score, game_over=False):
        """
        Render all game elements.
        """
        self.screen.fill(COLOR_BLACK)

        self.draw_grid()

        # Draw snake
        for pos in snake_positions:
            rect = pygame.Rect(pos[0]*CELL_SIZE, pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, COLOR_GREEN, rect)

        # Draw food
        if food_position:
            food_rect = pygame.Rect(food_position[0]*CELL_SIZE, food_position[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, COLOR_RED, food_rect)

        # Draw score
        score_surface = self.font.render(f'Score: {score}', True, COLOR_WHITE)
        self.screen.blit(score_surface, (10, 10))

        if game_over:
            self.draw_game_over()

        pygame.display.update()

    def draw_game_over(self):
        """
        Display Game Over message and options.
        """
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(COLOR_BLACK)
        self.screen.blit(overlay, (0, 0))

        large_font = pygame.font.SysFont('arial', 72)
        msg_surface = large_font.render('GAME OVER', True, COLOR_RED)
        msg_rect = msg_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
        self.screen.blit(msg_surface, msg_rect)

        small_font = pygame.font.SysFont('arial', 32)
        instr_surface = small_font.render('Press R to Restart or Q to Quit', True, COLOR_WHITE)
        instr_rect = instr_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 30))
        self.screen.blit(instr_surface, instr_rect)
