import requests
import pandas as pd
from tools import DB

NUM_PAGES = 100  # Number of TVmaze pages to fetch (each has ~250 shows)

def determine_genre_tag(genres):
    # Use "Anime" if any genre is anime, if not use the first genre or "Unknown" if empty
    if not genres:
        return "Unknown"
    return "Anime" if "anime" in [g.lower() for g in genres] else genres[0]

# DB helper
db = DB("data")
all_shows = {}

for page in range(NUM_PAGES):
    print(f"Fetching page {page} of popular shows...")
    response = requests.get(f"https://api.tvmaze.com/shows?page={page}")
    if response.status_code != 200:
        break  # Stop if request fails
    for show in response.json():
        show_id = show['id']
        if show_id in all_shows:
            continue  # Skip if already added
        genres = show.get('genres', [])
        all_shows[show_id] = {
            'id': show_id,
            'name': show.get('name'),
            'network': show['network']['name'] if show.get('network') else None,
            'genre_tag': determine_genre_tag(genres),
            'showType': show.get('type'),
            'country': show['network']['country']['name'] if show.get('network') and show['network'].get('country') else None,
            'language': show.get('language'),
            'premiered': show.get('premiered'),
            'runtime': show.get('runtime'),
            'rating': show['rating']['average'] if show.get('rating') and show['rating']['average'] is not None else None,
            'image': show['image']['medium'] if show.get('image') and show['image'].get('medium') else None
        }

# Convert to DataFrame and load into the database
df = pd.DataFrame(list(all_shows.values()))
db.load_from_dataframe(df, "shows")
print(f"✅ Loaded {len(df)} shows from TVmaze with all columns.")
