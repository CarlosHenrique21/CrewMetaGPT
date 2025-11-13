import os
import json
from pathlib import Path


class Config:
    CONFIG_DIR = Path.home() / '.weather-cli'
    CONFIG_FILE = CONFIG_DIR / 'config.json'

    def __init__(self):
        self.api_key = None
        self.default_unit = 'celsius'
        self._load_config()

    def _load_config(self):
        if not self.CONFIG_FILE.exists():
            # Create default config file with placeholder API key
            self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            self.api_key = ''
            default_config = {
                'api_key': '',
                'default_unit': 'celsius'
            }
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(default_config, f, indent=4)
        else:
            with open(self.CONFIG_FILE, 'r') as f:
                config = json.load(f)
                self.api_key = config.get('api_key', '')
                self.default_unit = config.get('default_unit', 'celsius')

    def save_config(self, api_key=None, default_unit=None):
        if api_key is not None:
            self.api_key = api_key
        if default_unit is not None:
            self.default_unit = default_unit

        config = {
            'api_key': self.api_key,
            'default_unit': self.default_unit
        }
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
