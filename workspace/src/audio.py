"""
Audio Module

Manages sound effects such as food consumption and game over signals.
"""

import pygame

class Audio:
    def __init__(self):
        pygame.mixer.init()
        try:
            self.eat_sound = pygame.mixer.Sound('assets/eat.wav')
        except Exception:
            self.eat_sound = None
        try:
            self.game_over_sound = pygame.mixer.Sound('assets/game_over.wav')
        except Exception:
            self.game_over_sound = None

    def play_eat(self):
        if self.eat_sound:
            self.eat_sound.play()

    def play_game_over(self):
        if self.game_over_sound:
            self.game_over_sound.play()
