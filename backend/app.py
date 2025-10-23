from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

DB_URI = "sqlite:///backend/data/spotify.db"
engine = create_engine(DB_URI)


@app.get("/api/stats")
def api_stats():
    view = request.args.get("view", "albums")
    limit = int(request.args.get("limit", 10))
    user = request.args.get("user", "badbunny")
    sort = request.args.get("sort", "total")

    user_path = os.path.join("backend", "data", "users", f"user_{user}.csv")
    full_library_path = os.path.join("backend", "data", "spotify_tracks.csv")

    if not os.path.exists(user_path):
        return jsonify({"error": f"User data not found: {user_path}"}), 404
    if not os.path.exists(full_library_path):
        return jsonify({"error": f"Spotify library not found: {full_library_path}"}), 404

    df_user = pd.read_csv(user_path)
    df_all = pd.read_csv(full_library_path)

    if view == "albums":
        liked_counts = (
            df_user.groupby(["track_album_id", "track_album_name"])
            .size()
            .reset_index(name="liked")
        )

        album_totals = (
            df_all.groupby(["track_album_id", "track_album_name"])
            .size()
            .reset_index(name="total")
        )

        result = liked_counts.merge(
            album_totals,
            on=["track_album_id", "track_album_name"],
            how="left"
        )

        result["percent"] = (result["liked"] / result["total"]) * 100
        result["percent"] = result["percent"].clip(upper=100)

        if sort == "percent":
            result = result.sort_values("percent", ascending=False)
        else:
            result = result.sort_values("liked", ascending=False)

        result = result.head(limit).reset_index(drop=True)

        data = []
        for i, row in result.iterrows():
            artist_list = df_user.loc[
                df_user["track_album_id"] == row.track_album_id, "track_artist"
            ].unique()
            artist_str = ", ".join(artist_list[:3])
            data.append({
                "rank": i + 1,
                "album": row.track_album_name,
                "artist": artist_str,
                "liked": int(row.liked),
                "total": int(row.total) if not pd.isna(row.total) else 0,
                "percent": round(row.percent, 1) if not pd.isna(row.percent) else 0.0
            })

    elif view == "artists":
        liked_counts = (
            df_user.groupby(["track_artist"])
            .size()
            .reset_index(name="liked")
        )

        artist_totals = (
            df_all.groupby(["track_artist"])
            .size()
            .reset_index(name="total")
        )

        result = liked_counts.merge(artist_totals, on="track_artist", how="left")
        result["percent"] = (result["liked"] / result["total"]) * 100
        result["percent"] = result["percent"].clip(upper=100)

        if sort == "percent":
            result = result.sort_values("percent", ascending=False)
        else:
            result = result.sort_values("liked", ascending=False)

        result = result.head(limit).reset_index(drop=True)

        data = []
        for i, row in result.iterrows():
            data.append({
                "rank": i + 1,
                "artist": row.track_artist,
                "liked": int(row.liked),
                "total": int(row.total) if not pd.isna(row.total) else 0,
                "percent": round(row.percent, 1) if not pd.isna(row.percent) else 0.0
            })

    else:
        return jsonify({"error": "Invalid view type. Must be 'albums' or 'artists'."}), 400

    return jsonify(data)


@app.get("/")
def index():
    return jsonify({"message": "Spotify Stats API running"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
