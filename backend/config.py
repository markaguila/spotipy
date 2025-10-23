import os

APP_ENV = os.getenv("APP_ENV", "development")
DB_URI = os.getenv("DB_URI", "sqlite:///backend/spotipy.db")
CSV_PATH = os.getenv("CSV_PATH", "backend/data/spotify_tracks.csv")
