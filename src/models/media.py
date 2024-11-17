from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Media:
    name: str
    media_type: str
    added_date: str = datetime.now().strftime("%Y-%m-%d")
    tmdb_id: Optional[int] = None
    overview: Optional[str] = None
    release_date: Optional[str] = None
    rating: Optional[float] = None 
    genres: List[str] = None
    
    user_rating: Optional[float] = None
    user_review: Optional[str] = None
    review_date: Optional[str] = None
    
    def __post_init__(self):
        if self.genres is None:
            self.genres = []
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "type": self.media_type,
            "added_date": self.added_date,
            "tmdb_id": self.tmdb_id,
            "overview": self.overview,
            "release_date": self.release_date,
            "rating": self.rating,
            "genres": self.genres,
            "user_rating": self.user_rating,
            "user_review": self.user_review,
            "review_date": self.review_date
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Media':
        return cls(
            name=data["name"],
            media_type=data["type"],
            added_date=data.get("added_date", datetime.now().strftime("%Y-%m-%d")),
            tmdb_id=data.get("tmdb_id"),
            overview=data.get("overview"),
            release_date=data.get("release_date"),
            rating=data.get("rating"),
            genres=data.get("genres", []),
            user_rating=data.get("user_rating"),
            user_review=data.get("user_review"),
            review_date=data.get("review_date")
        )

    def add_review(self, rating: float, review: str) -> None:
        self.user_rating = rating
        self.user_review = review
        self.review_date = datetime.now().strftime("%Y-%m-%d")