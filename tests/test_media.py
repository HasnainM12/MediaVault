import unittest
from datetime import datetime
from src.models.media import Media

class TestMedia(unittest.TestCase):
    def setUp(self):
        self.test_media = Media("Test Show", "TV Show")
    
    def test_media_creation(self):
        self.assertEqual(self.test_media.name, "Test Show")
        self.assertEqual(self.test_media.media_type, "TV Show")
        self.assertIsInstance(self.test_media.added_date, str)

    def test_to_dict(self):
        media_dict = self.test_media.to_dict()
        self.assertIsInstance(media_dict, dict)
        self.assertEqual(media_dict["name"], "Test Show")
        self.assertEqual(media_dict["type"], "TV Show")
        
    def test_from_dict(self):
        test_dict = {
            "name": "Another Show",
            "type": "Anime",
            "added_date": "2024-01-01"
        }
        media = Media.from_dict(test_dict)
        self.assertEqual(media.name, "Another Show")
        self.assertEqual(media.media_type, "Anime")
        self.assertEqual(media.added_date, "2024-01-01")

if __name__ == '__main__':
    unittest.main()