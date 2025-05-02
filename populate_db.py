import requests
import pandas as pd
from tools import DB

SEARCH_TERMS = [
    'comedy', 'drama', 'action', 'sci-fi', 'space', 'crime',
    'fantasy', 'thriller', 'animation', 'anime', 'romance', 'adventure',
    'superhero', 'reality', 'history', 'horror', 'documentary',
    'medical', 'teen', 'mystery', 'family', 'travel', 'sports',
    'korean', 'japanese', 'chinese', 'cantonese', 'french', 'german',
    'telenovela', 'game show', 'sitcom', 'martial arts', 'variety show',
    'idol', 'kids', 'cartoon', 'soap opera', 'donghua', 'manhua', 'c-drama'
]

db = DB("data")
all_shows = {}

for term in SEARCH_TERMS:
    print(f"Fetching: {term}")
    response = requests.get(f"https://api.tvmaze.com/search/shows?q={term}")
    if response.status_code == 200:
        for item in response.json():
            show = item['show']
            show_id = show['id']
            if show_id not in all_shows:
                all_shows[show_id] = {
                    'id': show_id,
                    'name': show.get('name'),
                    'summary': show.get('summary'),
                    'image': show['image']['medium'] if show.get('image') else None,
                    'genres': ','.join(show.get('genres', [])),
                    'genre_tag': show.get('genres')[0] if show.get('genres') else 'Unknown',
                    'rating': show['rating']['average'] if show.get('rating') else None,
                    'premiered': show.get('premiered'),
                    'language': show.get('language'),
                    'runtime': show.get('runtime'),
                    'country': show['network']['country']['name'] if show.get('network') and show['network'].get('country') else None,
                    'network': show['network']['name'] if show.get('network') else None
                }

df = pd.DataFrame(list(all_shows.values()))
db.load_from_dataframe(df, "shows")
print(f"✅ Loaded {len(df)} unique shows into the database.")


