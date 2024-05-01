import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import movieposters as mp

# Define your function to fetch IMDb links
def get_imdb_link(title):

    return mp.get_imdb_link_from_title(title)

# Read the CSV file into a DataFrame
df = pd.read_csv('Out_60.csv', lineterminator='\n')

# Define the number of concurrent threads
num_threads = 10

# Split the DataFrame into chunks for parallel processing
chunks = [df[i:i + num_threads] for i in range(0, len(df), num_threads)]

# Function to process each chunk
def process_chunk(chunk):
    links_list = []
    for title in chunk['title']:
        link = get_imdb_link(title)
        links_list.append(link)
    return links_list

# Process chunks in parallel
with ThreadPoolExecutor(max_workers=num_threads) as executor:
    results = executor.map(process_chunk, chunks)

# Merge results into the DataFrame
df['links'] = sum(results, [])

# Save the updated DataFrame
df.to_csv('Out_60_with_links.csv', index=False)
print('finished')