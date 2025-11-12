import json
import os

HIGH_SCORE_FILE = 'high_scores.json'

class Persistence:
    @staticmethod
    def load_high_scores():
        if not os.path.exists(HIGH_SCORE_FILE):
            return []
        try:
            with open(HIGH_SCORE_FILE, 'r') as f:
                data = json.load(f)
                return data.get('high_scores', [])
        except Exception:
            return []

    @staticmethod
    def save_high_score(player_name, score):
        scores = Persistence.load_high_scores()
        scores.append({'player': player_name, 'score': score})
        # Sort descending by score
        scores = sorted(scores, key=lambda x: x['score'], reverse=True)
        # Keep only top 10 scores
        scores = scores[:10]

        try:
            with open(HIGH_SCORE_FILE, 'w') as f:
                json.dump({'high_scores': scores}, f, indent=2)
        except Exception as e:
            print(f'Error saving high scores: {e}')
