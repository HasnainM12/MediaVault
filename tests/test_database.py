import unittest
import os
import json
import tempfile
from src.database import Database
from src.models.media import Media

class TestDatabase(unittest.TestCase):
    def setUp(self):
        
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_media_library.json")
        self.db = Database(self.db_path)
        
    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        os.rmdir(self.temp_dir)
        
    def test_save_and_load_data(self):
        test_media = [
            Media("Test Show 1", "TV Show"),
            Media("Test Show 2", "Movie")
        ]
        
        self.db.save_data(test_media)
        self.assertTrue(os.path.exists(self.db_path))
        
        loaded_media = self.db.load_data()
        self.assertEqual(len(loaded_media), 2)
        self.assertEqual(loaded_media[0].name, "Test Show 1")
        self.assertEqual(loaded_media[1].name, "Test Show 2")

    def test_empty_database(self):
        loaded_media = self.db.load_data()
        self.assertEqual(len(loaded_media), 0)

if __name__ == '__main__':
    unittest.main()