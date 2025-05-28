import requests
import pandas as pd
from tools import DB

# Cell 2: Constants and helper functions
NUM_PAGES = 100  # Number of TVmaze pages to fetch (each has ~250 shows)

def determine_genre_tag(genres):
    # Use "Anime" if any genre is anime, if not use the first genre or "Unknown" if empty
    if not genres:
        return "Unknown"
    return "Anime" if "anime" in [g.lower() for g in genres] else genres[0]
    
# Cell 3: DB helper and data structure
db = DB("data")
all_shows = {}

# Cell 4: Fetch shows from multiple genres
for page in range(NUM_PAGES):
    print(f"Fetching page {page} of popular shows...")
    response = requests.get(f"https://api.tvmaze.com/shows?page={page}")
    if response.status_code != 200:
        break # Stop if request fails
    for show in response.json():
        show_id = show['id']
        if show_id in all_shows:
            continue # Skip if already added
        genres = show.get('genres', [])
        # Store relevant show info
        all_shows[show_id] = {
            'id': show_id,
            'name': show.get('name'),
            'summary': show.get('summary'),
            'image': show['image']['medium'] if show.get('image') else None,
            'genres': ','.join(genres),
            'genre_tag': determine_genre_tag(genres),
            'showType': show.get('type', 'Unknown'),
            'rating': show['rating']['average'] if show.get('rating') else None,
            'premiered': show.get('premiered'),
            'language': show.get('language'),
            'runtime': show.get('runtime'),
            'country': show['network']['country']['name'] if show.get('network') and show['network'].get('country') else None,
            'network': show['network']['name'] if show.get('network') else None
        }

# Cell 5: Convert to DataFrame and load into the database
df = pd.DataFrame(list(all_shows.values()))
db.load_from_dataframe(df, "shows")
print(f"✅ Loaded {len(df)} shows from TVmaze with showType.")
