import json
from typing import List

class LocationManager:
    def __init__(self, storage_file: str = 'locations.json'):
        self.storage_file = storage_file

    def save_location(self, location: str) -> None:
        locations = self.load_locations()
        if location not in locations:
            locations.append(location)
            self._save_to_file(locations)

    def load_locations(self) -> List[str]:
        try:
            with open(self.storage_file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_to_file(self, locations: List[str]) -> None:
        with open(self.storage_file, 'w') as file:
            json.dump(locations, file)
