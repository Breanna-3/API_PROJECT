import requests
import pandas as pd
from tools import DB

GENRES = ['Comedy', 'Drama', 'Action', 'Science-Fiction']
API_URL = "https://api.tvmaze.com/search/shows?q="

db = DB("data")
all_shows = []

for genre in GENRES:
    response = requests.get(API_URL + genre)
    if response.status_code == 200:
        data = response.json()
        for item in data:
            show = item['show']
            all_shows.append({
                'id': show['id'],
                'name': show['name'],
                'summary': show['summary'],
                'image': show['image']['medium'] if show.get('image') else None,
                'genres': ','.join(show.get('genres', [])),
                'genre_tag': genre
            })

df = pd.DataFrame(all_shows).drop_duplicates(subset=['id'])
db.load_from_dataframe(df, "shows")
print(f"Loaded {len(df)} shows into the database.")

