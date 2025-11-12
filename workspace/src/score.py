"""
Score module.
Tracks current score and manages high score persistence.
"""
import json
import os
from src.config import HIGHSCORE_FILE

class Score:
    def __init__(self):
        self.current_score = 0
        self.high_score = 0
        self.load_high_score()

    def increase(self, points=1):
        self.current_score += points

    def reset(self):
        self.current_score = 0

    def load_high_score(self):
        if os.path.exists(HIGHSCORE_FILE):
            try:
                with open(HIGHSCORE_FILE, 'r') as f:
                    data = json.load(f)
                    self.high_score = data.get('high_score', 0)
            except (json.JSONDecodeError, IOError):
                self.high_score = 0
        else:
            self.high_score = 0

    def save_high_score(self):
        if self.current_score > self.high_score:
            self.high_score = self.current_score
            try:
                with open(HIGHSCORE_FILE, 'w') as f:
                    json.dump({'high_score': self.high_score}, f)
            except IOError:
                pass
