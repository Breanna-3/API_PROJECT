import requests
import pandas as pd
from tools import DB

NUM_PAGES = 100  # Number of TVmaze pages to fetch (each has ~250 shows- rougly 25000 shows generated)



db = DB("data")
all_shows = {}

for page in range(NUM_PAGES):
    print(f"Fetching page {page} of popular shows...")
    response = requests.get(f"https://api.tvmaze.com/shows?page={page}")
    if response.status_code != 200:
        break
    for show in response.json():
        show_id = show['id']
        if show_id in all_shows:
            continue
        genres = show.get('genres', [])
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

df = pd.DataFrame(list(all_shows.values()))
db.load_from_dataframe(df, "shows")
print(f"✅ Loaded {len(df)} shows from TVmaze with showType.")
