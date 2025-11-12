import pygame
import os

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.enabled = True
        try:
            self.eat_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'eat.wav'))
            self.game_over_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'game_over.wav'))
            self.pause_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), 'pause.wav'))
        except pygame.error:
            self.enabled = False

    def play_eat(self):
        if self.enabled:
            self.eat_sound.play()

    def play_game_over(self):
        if self.enabled:
            self.game_over_sound.play()

    def play_pause(self):
        if self.enabled:
            self.pause_sound.play()
