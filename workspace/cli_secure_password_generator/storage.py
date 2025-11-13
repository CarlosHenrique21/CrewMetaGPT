import json
import os

class Storage:
    def __init__(self, filename: str):
        self.filename = filename
        self.data = self.load_data()

    def load_data(self):
        # Load data from JSON file if it exists
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        return {}

    def save_data(self):
        # Save data to JSON file
        with open(self.filename, 'w') as file:
            json.dump(self.data, file, indent=4)

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value
        self.save_data()