import pygame

class UIRenderer:
    CELL_SIZE = 20
    BORDER_COLOR = (50, 50, 50)
    SNAKE_COLOR = (0, 255, 0)
    FOOD_COLOR = (255, 0, 0)
    BG_COLOR = (0, 0, 0)
    TEXT_COLOR = (255, 255, 255)
    FONT_SIZE = 24

    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        window_width = width * self.CELL_SIZE
        window_height = height * self.CELL_SIZE + 40  # Extra for score
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption('CLI Snake Game')
        self.font = pygame.font.SysFont(None, self.FONT_SIZE)

    def render(self, snake, food, score, game_over, paused, running):
        self.screen.fill(self.BG_COLOR)

        # Draw grid (optional, lightly)
        for x in range(0, self.width * self.CELL_SIZE, self.CELL_SIZE):
            pygame.draw.line(self.screen, self.BORDER_COLOR, (x, 0), (x, self.height * self.CELL_SIZE))
        for y in range(0, self.height * self.CELL_SIZE, self.CELL_SIZE):
            pygame.draw.line(self.screen, self.BORDER_COLOR, (0, y), (self.width * self.CELL_SIZE, y))

        # Draw snake
        for segment in snake:
            rect = pygame.Rect(segment[0]*self.CELL_SIZE, segment[1]*self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
            pygame.draw.rect(self.screen, self.SNAKE_COLOR, rect)

        # Draw food
        food_rect = pygame.Rect(food[0]*self.CELL_SIZE, food[1]*self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
        pygame.draw.rect(self.screen, self.FOOD_COLOR, food_rect)

        # Draw score
        score_surface = self.font.render(f'Score: {score}', True, self.TEXT_COLOR)
        self.screen.blit(score_surface, (5, self.height * self.CELL_SIZE + 5))

        # Draw game state messages
        if not running and not paused and not game_over:
            msg = 'Press any arrow key to start'
            self.draw_centered_text(msg)
        elif paused:
            msg = 'Game Paused - Press P to resume'
            self.draw_centered_text(msg)
        elif game_over:
            msg = 'Game Over - Press R to Restart'
            self.draw_centered_text(msg)

        pygame.display.flip()

    def draw_centered_text(self, text):
        text_surface = self.font.render(text, True, self.TEXT_COLOR)
        rect = text_surface.get_rect(center=(self.width * self.CELL_SIZE // 2, self.height * self.CELL_SIZE // 2))
        self.screen.blit(text_surface, rect)

    def cleanup(self):
        pygame.quit()
