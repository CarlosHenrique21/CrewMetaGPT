"""
Main entry point for CLI Snake Game with Pygame.
Manages initialization, game loop, and restart/exit options.
"""
import sys
import pygame
from src.config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from src.input_handler import InputHandler
from src.renderer import Renderer
from src.game import Game


def main():
    pygame.init()
    pygame.display.set_caption('CLI Snake Game')

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('arial', 24)

    renderer = Renderer(screen, font)
    input_handler = InputHandler()
    game = Game()

    running = True
    while running:
        # Process input
        input_result = input_handler.process_events()
        if input_result == 'QUIT':
            running = False
            break

        # Update game state
        if not game.is_game_over():
            game.update(input_result)
        else:
            # Show game over screen and wait for restart or quit
            renderer.render(game.get_snake_positions(), game.get_food_position(), game.get_score(), game_over=True)

            # Handle restart/quit input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game.reset()
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        running = False

            clock.tick(FPS)
            continue

        # Render current game state
        renderer.render(game.get_snake_positions(), game.get_food_position(), game.get_score())

        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
