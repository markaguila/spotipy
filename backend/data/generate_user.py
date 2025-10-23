import pandas as pd
import os

# Paths
library_path = os.path.join("backend", "data", "spotify_tracks.csv")
output_dir = os.path.join("backend", "data", "users")
os.makedirs(output_dir, exist_ok=True)

# Load full Spotify library
df = pd.read_csv(library_path)

# Filter for Bad Bunny
df_badbunny = df[df["track_artist"].str.contains("Bad Bunny", case=False, na=False)]

# Pick 10 random Bad Bunny tracks (or all if less)
df_user = df_badbunny.sample(n=min(10, len(df_badbunny)), random_state=42)

# Save to user folder
output_path = os.path.join(output_dir, "user_badbunny.csv")
df_user.to_csv(output_path, index=False)

print(f" Created simulated user library: {output_path}")
print(f"Contains {len(df_user)} tracks by Bad Bunny.")
