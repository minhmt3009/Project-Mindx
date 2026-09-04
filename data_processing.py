import pandas as pd 
df = pd.read_csv(r'D:\Data Science\Project cuối khóa 1 Mindx\spotify_data_processed.csv')

# Get list of all tracks (payload optimized)
def get_all_track(df: pd.DataFrame):
    cols = ['track_id', 'track_name', 'artist_name', 'genre', 'label', 'country', 'release_year', 'stream_count', 'popularity']
    available_cols = [c for c in cols if c in df.columns]
    return df[available_cols].to_dict(orient = 'records')



# Filter tracks by genre
def filter_by_genre(df: pd.DataFrame, genre):
    if genre.lower() not in df['genre'].str.lower().values:
        return {'error': 'Genre does not exist in the dataset'}
    result = df[df['genre'].str.lower() == genre.lower()]
    return result.to_dict(orient = 'records')


# Filter tracks by artist
def filter_by_artist(df: pd.DataFrame, artist):
    if artist.lower() not in df['artist_name'].str.lower().values:
        return {'error': 'Artist not found in the dataset'}
    result = df[df['artist_name'].str.lower() == artist.lower()]
    return result.to_dict(orient = 'records')


# Filter tracks by release year
def filter_by_year(df: pd.DataFrame, year):
    if year not in df['release_year'].values:
        return {'error': 'Release year not found in the dataset, please choose another year'}
    result = df[df['release_year'] == year]
    return result.to_dict(orient = 'records')


# Filter tracks by record label
def filter_by_label(df: pd.DataFrame, label):
    if label.lower() not in df['label'].str.lower().values:
        return {'error': 'Label not found in the dataset, please re-enter'}
    result = df[df['label'].str.lower() == label.lower()]
    return result.to_dict(orient = 'records')


# Filter tracks by country
def filter_by_country(df: pd.DataFrame, country):
    if country.lower() not in df['country'].str.lower().values:
        return {'error': 'Country not found in the dataset'}
    result = df[df['country'].str.lower() == country.lower()]
    return result.to_dict(orient = 'records')


# Filter tracks by loudness category
def filter_by_loudness(df: pd.DataFrame, loudness):
    if loudness.lower() not in df['loudness_category'].str.lower().values:
        return {'error': 'Loudness category does not exist'}
    result = df[df['loudness_category'].str.lower() == loudness.lower()]
    return result.to_dict(orient = 'records')


# Get track by track ID
def get_trackid(df: pd.DataFrame, trackid):
    if trackid.lower() not in df['track_id'].str.lower().values:
        return {'error': 'Track ID does not exist'}
    result = df[df['track_id'].str.lower() == trackid.lower()]
    return result.to_dict(orient = 'records')


# Get track by track name
def get_song(df: pd.DataFrame, song):
    if song.lower() not in df['track_name'].str.lower().values:
        return {'error': 'Track not found'}
    result = df[df['track_name'].str.lower() == song.lower()]
    return result.to_dict(orient = 'records')


# Suggest track names based on keyword query
def suggest_song_names(df: pd.DataFrame, query: str, limit: int = 10):
    if not query or not isinstance(query, str) or not query.strip():
        return []
    query_clean = query.strip().lower()
    matches = df[df['track_name'].str.lower().str.contains(query_clean, na=False)]
    if matches.empty:
        return []
    cols = ['track_id', 'track_name', 'artist_name', 'genre']
    available_cols = [c for c in cols if c in df.columns]
    return matches[available_cols].head(limit).to_dict(orient = 'records')
