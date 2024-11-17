from typing import Dict, List, Optional
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class TMDBApi:
    def __init__(self):
        self.api_key = os.getenv('TMDB_API_KEY')
        self.base_url = "https://api.themoviedb.org/3"
        
        if not self.api_key:
            raise ValueError("TMDB API key not found in environment variables")
    
    def search_media(self, query: str, media_type: str = "movie") -> List[Dict]:
        """
        Search for movies or TV shows
        
        Args:
            query (str): Search term
            media_type (str): Either 'movie' or 'tv'
            
        Returns:
            List[Dict]: List of search results
        """
        endpoint = f"{self.base_url}/search/{media_type}"
        params = {
            "api_key": self.api_key,
            "query": query,
            "language": "en-US",
            "page": 1
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()["results"]
        except requests.RequestException as e:
            print(f"Error fetching data from TMDB: {e}")
            return []
    
    def get_details(self, media_id: int, media_type: str = "movie") -> Optional[Dict]:
        """
        Get detailed information about a specific movie or TV show
        
        Args:
            media_id (int): TMDB ID of the media
            media_type (str): Either 'movie' or 'tv'
            
        Returns:
            Optional[Dict]: Detailed information about the media
        """
        endpoint = f"{self.base_url}/{media_type}/{media_id}"
        params = {
            "api_key": self.api_key,
            "language": "en-US"
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching details from TMDB: {e}")
            return None