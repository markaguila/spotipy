from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine, text
from backend.config import DB_URI

app = Flask(__name__)
CORS(app)

engine = create_engine(DB_URI)

@app.get("/api/stats")
def api_stats():
    view = request.args.get("view", "albums")
    limit = int(request.args.get("limit", 10))

    if view == "albums":
        query = text("""
            SELECT album_name, artist_name, track_count
            FROM albums
            ORDER BY track_count DESC
            LIMIT :limit
        """)
    else:
        query = text("""
            SELECT artist_name, track_count
            FROM artists
            ORDER BY track_count DESC
            LIMIT :limit
        """)

    with engine.connect() as conn:
        rows = conn.execute(query, {"limit": limit}).fetchall()

    if view == "albums":
        results = [
            {
                "rank": i + 1,
                "album": row.album_name,
                "artist": row.artist_name,
                "liked": None,
                "total": row.track_count,
                "percent": None
            }
            for i, row in enumerate(rows)
        ]
    else:
        results = [
            {
                "rank": i + 1,
                "artist": row.artist_name,
                "liked": None,
                "total": row.track_count,
                "percent": None
            }
            for i, row in enumerate(rows)
        ]

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
