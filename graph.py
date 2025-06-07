import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("imdb_popular_movies.csv")

# Convert 'votes' column from strings to actual numbers
def parse_votes(v):
    if pd.isna(v) or v == '':
        return None
    if isinstance(v, str):
        if 'K' in v:
            return float(v.replace('K', '')) * 1_000
    return float(v)

df['votes'] = df['votes'].apply(parse_votes)

# Clean data
df_clean = df.dropna(subset=['votes']).copy()

# Bar Chart - All movies by number of votes
plt.figure(figsize=(10, 8)) 
df_sorted = df_clean.sort_values(by='votes', ascending=False)

plt.barh(df_sorted['title'], df_sorted['votes'], color='skyblue')
plt.xlabel('Votes (in thousands)', fontsize=12)
plt.ylabel('Movie Title', fontsize=12)
plt.title('All IMDb Movies by Number of Votes', fontsize=14, pad=20)
plt.grid(axis='x', linestyle='--', alpha=0.6)

plt.barh(df_sorted['title'], df_sorted['votes'], color='skyblue')
plt.gca().invert_yaxis()

# Format x-axis to show K for thousands
def format_votes(x, _):
    if x >= 1_000:
        return f'{x/1_000:.0f}K'
    return f'{x:.0f}'

plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(format_votes))
plt.tight_layout()
plt.show()

