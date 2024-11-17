import json
import os
from typing import List
from models.media import Media #REMEMBER: runs from app.py

class Database:
    def __init__(self, file_path: str = "data/media_library.json"):
        self.file_path = file_path
        self.ensure_data_file()

    def ensure_data_file(self) -> None:
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
        if not os.path.exists(self.file_path):
            self.save_data([])

    def load_data(self) -> List[Media]:
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                return [Media.from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):

            self.save_data([])
            return []

    def save_data(self, media_list: List[Media]) -> None:

        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
        with open(self.file_path, 'w') as f:
            json.dump([media.to_dict() for media in media_list], f, indent=4)