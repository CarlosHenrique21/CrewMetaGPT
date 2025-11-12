import pygame
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE, COLOR_BLACK, COLOR_GREEN, COLOR_RED, COLOR_WHITE, COLOR_GRAY, STATE_GAMEOVER

class Renderer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('CLI Snake Game')
        self.font = pygame.font.SysFont('Arial', 24)
        self.clock = pygame.time.Clock()

    def draw_block(self, color, position):
        x, y = position
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(self.screen, color, rect)

    def draw(self, game_state):
        self.screen.fill(COLOR_BLACK)

        # Draw snake
        for segment in game_state['snake']:
            self.draw_block(COLOR_GREEN, segment)

        # Draw food
        self.draw_block(COLOR_RED, game_state['food'])

        # Draw score
        score_surface = self.font.render(f'Score: {game_state["score"]}', True, COLOR_WHITE)
        self.screen.blit(score_surface, (10, 10))

        # Draw game over message
        if game_state['state'] == STATE_GAMEOVER:
            game_over_surf = self.font.render('GAME OVER! Press R to Restart or Q to Quit.', True, COLOR_GRAY)
            rect = game_over_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(game_over_surf, rect)

        pygame.display.flip()

    def tick(self, fps):
        self.clock.tick(fps)

    def quit(self):
        pygame.quit()
