import json
from pathlib import Path
from errors import FavoriteError


class FavoritesManager:
    FAVORITES_DIR = Path.home() / '.weather-cli'
    FAVORITES_FILE = FAVORITES_DIR / 'favorites.json'

    def __init__(self):
        self.FAVORITES_DIR.mkdir(exist_ok=True, parents=True)
        if not self.FAVORITES_FILE.exists():
            with open(self.FAVORITES_FILE, 'w') as f:
                json.dump({'favorites': []}, f)

    def _load_favorites(self):
        try:
            with open(self.FAVORITES_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise FavoriteError(f'Error loading favorites: {str(e)}')

    def _save_favorites(self, data):
        try:
            with open(self.FAVORITES_FILE, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            raise FavoriteError(f'Error saving favorites: {str(e)}')

    def list_favorites(self):
        data = self._load_favorites()
        return data.get('favorites', [])

    def add_favorite(self, name, location):
        data = self._load_favorites()
        favorites = data.get('favorites', [])
        if any(fav['name'].lower() == name.lower() for fav in favorites):
            raise FavoriteError(f'Favorite with name "{name}" already exists')
        favorites.append({'name': name, 'location': location})
        data['favorites'] = favorites
        self._save_favorites(data)

    def remove_favorite(self, name):
        data = self._load_favorites()
        favorites = data.get('favorites', [])
        filtered = [fav for fav in favorites if fav['name'].lower() != name.lower()]
        if len(filtered) == len(favorites):
            raise FavoriteError(f'Favorite with name "{name}" not found')
        data['favorites'] = filtered
        self._save_favorites(data)

    def get_location_by_name(self, name):
        data = self._load_favorites()
        favorites = data.get('favorites', [])
        for fav in favorites:
            if fav['name'].lower() == name.lower():
                return fav['location']
        return None
