from typing import Dict, List, Optional
import requests
import time

class JikanApi:
    def __init__(self):
        self.base_url = "https://api.jikan.moe/v4"
        self.last_request = 0
        self.rate_limit = 1  # Minimum seconds between requests
        
    def _respect_rate_limit(self):
        """Ensure we don't exceed Jikan's rate limit"""
        current_time = time.time()
        time_passed = current_time - self.last_request
        if time_passed < self.rate_limit:
            time.sleep(self.rate_limit - time_passed)
        self.last_request = time.time()
        
    def search_anime(self, query: str) -> List[Dict]:
        """
        Search for anime by title
        
        Args:
            query (str): Search term
            
        Returns:
            List[Dict]: List of search results
        """
        self._respect_rate_limit()
        endpoint = f"{self.base_url}/anime"
        params = {
            "q": query,
            "limit": 10
        }
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()["data"]
        except requests.RequestException as e:
            print(f"Error fetching data from Jikan: {e}")
            return []
    
    def get_anime_details(self, anime_id: int) -> Optional[Dict]:
        """
        Get detailed information about a specific anime
        
        Args:
            anime_id (int): MyAnimeList ID of the anime
            
        Returns:
            Optional[Dict]: Detailed information about the anime
        """
        self._respect_rate_limit()
        endpoint = f"{self.base_url}/anime/{anime_id}/full"
        
        try:
            response = requests.get(endpoint)
            response.raise_for_status()
            return response.json()["data"]
        except requests.RequestException as e:
            print(f"Error fetching anime details from Jikan: {e}")
            return None