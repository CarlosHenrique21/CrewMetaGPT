import pygame
from src.constants import FPS, STATE_GAMEOVER
from src.game_engine import GameEngine
from src.input_handler import InputHandler
from src.renderer import Renderer
from src.persistence import Persistence


def main():
    pygame.init()
    input_handler = InputHandler()
    game_engine = GameEngine()
    renderer = Renderer()

    running = True

    while running:
        direction = input_handler.get_latest_direction()

        if direction is None:
            # Quit event received
            running = False
            continue

        if game_engine.state == STATE_GAMEOVER:
            # Check for restart or quit
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                game_engine.reset()
            elif keys[pygame.K_q]:
                running = False
            # Still render game over
            renderer.draw(game_engine.get_state())
            renderer.tick(FPS)
            continue

        # Update game state
        game_engine.update(direction)

        # Render
        renderer.draw(game_engine.get_state())
        renderer.tick(FPS)

    # On exit, save high score
    final_score = game_engine.score
    if final_score > 0:
        # For simplicity, save with player name 'player'
        Persistence.save_high_score('player', final_score)

    renderer.quit()
    pygame.quit()


if __name__ == '__main__':
    main()
