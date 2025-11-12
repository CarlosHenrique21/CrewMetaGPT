import json
import os

class DataPersistence:
    def __init__(self, leaderboard_file='data/leaderboard.json'):
        self.leaderboard_file = leaderboard_file

    def load_high_scores(self):
        try:
            if not os.path.exists(self.leaderboard_file):
                return {}
            with open(self.leaderboard_file, 'r') as f:
                data = json.load(f)
                scores = {entry['player']: entry['score'] for entry in data.get('leaderboard', [])}
                return scores
        except (IOError, json.JSONDecodeError):
            # Return empty dict if error occurs
            return {}

    def save_high_scores(self, scores):
        # scores is dict player->score
        data = {'leaderboard': [{'player': player, 'score': score} for player, score in scores.items()]}
        try:
            with open(self.leaderboard_file, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError:
            # Could log error if needed
            pass
