from sqlalchemy import create_engine, text
from backend.config import DB_URI

engine = create_engine(DB_URI)

print("Checking database contents...\n")

with engine.connect() as conn:
    # --- Top 5 albums ---
    print("Top 5 Albums by Track Count:")
    query_albums = text("""
        SELECT album_name, artist_name, track_count
        FROM albums
        ORDER BY track_count DESC
        LIMIT 5;
    """)
    rows = conn.execute(query_albums).fetchall()
    for row in rows:
        print(f"- {row.album_name} by {row.artist_name} ({row.track_count} tracks)")

    # --- Top 5 artists ---
    print("\nTop 5 Artists by Track Count:")
    query_artists = text("""
        SELECT artist_name, track_count
        FROM artists
        ORDER BY track_count DESC
        LIMIT 5;
    """)
    rows = conn.execute(query_artists).fetchall()
    for row in rows:
        print(f"- {row.artist_name} ({row.track_count} tracks)")
