# MediaVault

A web application I built to track my movies, TV shows, and anime collection. It uses TMDB and MyAnimeList APIs to fetch media information and lets me add personal ratings and reviews.

## Features

- Track movies, TV shows, and anime
- Search through TMDB and MyAnimeList databases
- Add personal ratings and reviews
- Clean interface using Tailwind CSS

## Built With

- Python/Flask
- TMDB & Jikan APIs
- HTML/Tailwind CSS
- JSON storage

## Setup

Create and activate virtual environment:

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin activate  # Mac/Linux
```

Install requirements:

```bash
pip install -r requirements.txt
```

Remember to:

- Add TMDB API key to .env file
- Run from project root: `python src/app.py`
- Run deactivate before instantiating another virtual environment

## Future Plans

- User accounts
- Better search filters
- Watchlist feature
- More anime tracking features
- Polished UI
