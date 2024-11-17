import pytest
import os
import sys

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, src_path)




@pytest.fixture
def sample_media_data():

    return [
        {
            "name": "Test Show",
            "type": "TV Show",
            "added_date": "2024-01-01"
        },
        {
            "name": "Test Movie",
            "type": "Movie",
            "added_date": "2024-01-01"
        }
    ]