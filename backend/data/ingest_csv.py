import pandas as pd
from sqlalchemy import create_engine
from backend.models.db_setup import Base, Album, Artist
from backend.config import DB_URI, CSV_PATH

# --- Step 1: Load CSV ---
print(f"Loading data from {CSV_PATH}...")
df = pd.read_csv(CSV_PATH)

# --- Step 2: Preview columns ---
print(f"Columns found: {list(df.columns)}")

# --- Step 3: Validate required columns ---
required_cols = ["track_album_name", "track_album_id", "track_artist", "track_id"]
missing = [col for col in required_cols if col not in df.columns]
if missing:
    raise ValueError(f"Missing expected columns: {missing}")

# --- Step 4: Create database and tables ---
engine = create_engine(DB_URI)
Base.metadata.create_all(engine)

# --- Step 5: Compute track counts per album ---
album_counts = (
    df.groupby(["track_album_id", "track_album_name", "track_artist"])
      .agg(track_count=("track_id", "count"))
      .reset_index()
)

# --- Step 6: Compute track counts per artist ---
artist_counts = (
    df.groupby(["track_artist"])
      .agg(track_count=("track_id", "count"))
      .reset_index()
)

# --- Step 7: Prepare DataFrames for SQL ---
albums_df = album_counts.rename(columns={
    "track_album_id": "album_id",
    "track_album_name": "album_name",
    "track_artist": "artist_name"
})
albums_df["artist_id"] = None  # Placeholder, Spotify artist ID not in CSV

artists_df = artist_counts.rename(columns={
    "track_artist": "artist_name"
})
artists_df["artist_id"] = None  # Placeholder, Spotify artist ID not in CSV

# --- Step 8: Insert into SQL tables ---
print(f"Inserting {len(albums_df)} albums and {len(artists_df)} artists into database...")
albums_df.to_sql(Album.__tablename__, engine, if_exists="replace", index=False)
artists_df.to_sql(Artist.__tablename__, engine, if_exists="replace", index=False)

print("Done! Database populated successfully.")
