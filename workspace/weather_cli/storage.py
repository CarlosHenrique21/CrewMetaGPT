import json

class Storage:
    @staticmethod
    def read_file(file_path: str):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    @staticmethod
    def write_file(file_path: str, data: dict) -> None:
        with open(file_path, 'w') as file:
            json.dump(data, file)
