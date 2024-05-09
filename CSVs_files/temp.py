from http.client import IncompleteRead
import time
import movieposters.errors
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import movieposters as mp

def get_imdb_link(title):
    return mp.get_imdb_link_from_title(title)

def get_poster_link(imdb_link):
    retries = 3
    for _ in range(retries):
        try:
            return mp.get_poster_from_imdb_link(imdb_link)
        except IncompleteRead:
            time.sleep(1)  # Wait for a second before retrying
            continue
    return 'N/A'  # Return a fallback value if all retries fail

df = pd.read_csv('orig_movie.csv', lineterminator='\n')
num_threads = 20
chunks = [df[i:i + num_threads] for i in range(0, len(df), num_threads)]
total_chunks = len(chunks)
processed_chunks = 0

def process_chunk(chunk):
    imdb_links_list = []
    poster_links_list = []
    for title in chunk['title']:
        try:
            imdb_link = get_imdb_link(title)
            poster_link = get_poster_link(imdb_link)
            imdb_links_list.append(imdb_link)
            poster_links_list.append(poster_link)
        except movieposters.errors.MovieNotFound:
            pass
    return imdb_links_list, poster_links_list

with ThreadPoolExecutor(max_workers=num_threads) as executor:
    results = executor.map(process_chunk, chunks)

    for result in results:
        processed_chunks += 1
        progress = processed_chunks / total_chunks * 100
        print(f"Processed {processed_chunks}/{total_chunks} chunks ({progress:.2f}%)")

imdb_links = []
poster_links = []
for imdb, poster in results:
    imdb_links.extend(imdb)
    poster_links.extend(poster)
df['imdb_link'] = imdb_links
df['poster_link'] = poster_links

df.to_csv('orig_movie_with_links', index=False)
print('finished')
