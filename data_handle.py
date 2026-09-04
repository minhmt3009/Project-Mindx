import pandas as pd
df = pd.read_csv(r'D:\Data Science\Project cuối khóa 1 Mindx\spotify_data_processed.csv')
from datetime import date

# Auto-generate new track ID
def new_trackid(df: pd.DataFrame):
    if df.empty:
        return 'TRK-00001'

    numeric_parts = df["track_id"].str.replace("TRK-", "", regex=False).astype(int)
    next_number = numeric_parts.max() + 1
    
    return f"TRK-{next_number:05d}" 

default_values = {'album_name':'', 'duration_ms': 0, 'popularity': 50, 'stream_count':1000 }
required_values = ['track_name', 'artist_name', 'genre', 'country', 'label', 'loudness_category', 'release_date']


# Format and parse date
def parse_new_date(data: dict) -> pd.Timestamp:
    new_date = data.get('release_date')

    if not new_date:
        # Default to today if date is not provided
        return pd.Timestamp(date.today())

    try:
        return pd.to_datetime(new_date)
    except (ValueError, TypeError):
        return {'error': 'Invalid date format'}



# Create new track record
def create_new_track (data: dict, df: pd.DataFrame) -> dict:
    missing = [f for f in required_values if not data.get(f)]
    if missing:
        return {'error': f'Missing required fields: {missing}'}


    new_id = new_trackid(df)
    release_date = parse_new_date(data)

    new_track_song = {
        'track_id': new_id,
        'track_name': data.get('track_name'),
        'artist_name': data.get('artist_name'),
        'country': data.get('country') or '',
        'label': data.get('label') or 'Independent',
        'genre': data.get('genre') or 'Unknown',
        'loudness_category': data.get('loudness_category') or 'Moderate',
        'release_date': release_date.strftime('%Y-%m-%d'),
        'release_year': release_date.year,
        'release_month': release_date.month,
        'release_day_of_week': release_date.day_name(),
        **default_values
    }

    return new_track_song



# Delete track by track ID
def delete_track(df: pd.DataFrame, track_id: str):
    if not track_id:
        return {'error': 'Track ID is required'}

    if track_id.lower() not in df['track_id'].str.lower().values:
        return {'error': 'Track ID does not exist'}

    del_id = df.index[df['track_id'].str.lower() == track_id.lower()]
    if del_id.empty:
        return {'error': 'Track ID not found'}

    df = df.drop(index=del_id[0]).reset_index(drop=True)
    return df


# Get song suggestions for autocomplete / search
def get_song_suggestions(df: pd.DataFrame, query: str, limit: int = 10):
    if not query or not isinstance(query, str) or not query.strip():
        return []
    query_clean = query.strip().lower()
    matches = df[df['track_name'].str.lower().str.contains(query_clean, na=False)]
    if matches.empty:
        return []
    cols = ['track_id', 'track_name', 'artist_name', 'genre', 'label', 'country', 'release_year']
    available_cols = [c for c in cols if c in df.columns]
    return matches[available_cols].head(limit).to_dict(orient='records')


# Delete track by song name (with suggestion support if multiple matches or ambiguous)
def delete_track_by_song(df: pd.DataFrame, song_name: str, track_id: str = None):
    if not song_name or not isinstance(song_name, str) or not song_name.strip():
        return {'error': 'Song name is required'}

    clean_song_name = song_name.strip()

    # If track_id is explicitly provided for exact disambiguation
    if track_id:
        return delete_track(df, track_id)

    # Search for exact matches (case-insensitive)
    exact_matches = df[df['track_name'].str.lower() == clean_song_name.lower()]

    if exact_matches.empty:
        # Search for partial match suggestions
        suggestions = get_song_suggestions(df, clean_song_name)
        if suggestions:
            return {
                'error': f"Track '{clean_song_name}' not found exact match. Did you mean one of the suggested tracks below?",
                'suggestions': suggestions
            }
        return {'error': f"Track '{clean_song_name}' not found in the dataset"}

    # If multiple tracks have the exact same song name, return all matches with IDs for user selection
    if len(exact_matches) > 1:
        cols = ['track_id', 'track_name', 'artist_name', 'genre', 'label', 'release_year']
        available_cols = [c for c in cols if c in df.columns]
        suggestions = exact_matches[available_cols].to_dict(orient='records')
        return {
            'error': f"Multiple tracks found with name '{clean_song_name}'. Please select the specific track from suggestions to delete.",
            'suggestions': suggestions
        }

    # Exactly one matching track found -> delete it
    del_idx = exact_matches.index[0]
    df = df.drop(index=del_idx).reset_index(drop=True)
    return df


default_cols = ['genre', 'country', 'label', 'track_id', 'track_name', 'artist_name', 'release_date', 'stream_count', 'popularity']

# Find top tracks with highest stream count
def get_top_track(df: pd.DataFrame, top: int):
    highest = df.nlargest(top, 'stream_count')[default_cols].reset_index(drop=True)
    return highest.to_dict(orient = 'records')


# Find bottom tracks with lowest stream count
def get_bottom_track(df: pd.DataFrame, bot: int):
    lowest = df.nsmallest(bot, 'stream_count')[default_cols].reset_index(drop=True)
    return lowest.to_dict(orient = 'records')


# Rank tracks by popularity score
def get_top_popularity(df: pd.DataFrame, top: int):
    most = df.nlargest(top, 'popularity')[default_cols].reset_index(drop=True)
    return most.to_dict(orient = 'records')


# Total stream count by genre
def top_genre(df: pd.DataFrame, top: int = None):
    genrecount = (df.groupby('genre')['stream_count']
            .sum()
            .reset_index()
            .sort_values('stream_count', ascending = False)
            .reset_index(drop = True)
            )

    if top is not None:
        genrecount = genrecount.nlargest(top, 'stream_count')
    return genrecount.to_dict(orient = 'records')



# Total stream count by year
def top_year(df: pd.DataFrame, top: int = None):
    yearcount = (df.groupby('release_year')['stream_count']
            .sum()
            .reset_index()
            .sort_values('release_year', ascending = True)
            .reset_index(drop = True)
            )
    
    if top is not None:
        yearcount = yearcount.nlargest(top, 'stream_count')
    return yearcount.to_dict(orient = 'records')



# Average popularity by genre => categorize into: Very popular, Popular, Unpopular
def classify_popularity(score):
    if score >= 70:
        return 'Very popular'
    elif score >= 40:
        return 'Popular'
    elif score <= 0:
        return {'error': 'Score must be greater than 0'}
    else:
        return 'Unpopular'


def avg_pop(df: pd.DataFrame):
    df = df.copy()
    avg = (df.groupby('genre')['popularity']
        .mean()
        .reset_index()
        .sort_values('popularity', ascending = False)
        .reset_index(drop = True)
        )
    avg['category'] = avg['popularity'].apply(classify_popularity)

    return avg.to_dict(orient = 'records')



# Track count by quarter across all years
def classify_quarter(month: int):
    if 1 <= month <= 3:
        return 'Quarter I'
    elif 4 <= month <= 6:
        return 'Quarter II'
    elif 7 <= month <= 9:
        return 'Quarter III'
    elif 10 <= month <= 12:
        return 'Quarter IV'
    else: 
        return 'Unknown'


def month_track_count(df: pd.DataFrame):
    df = df.copy()
    df['category'] = df['release_month'].apply(classify_quarter)

    quartercount = (df.groupby('category')['track_id']
                .nunique()
                .reset_index()
                .rename(columns={'track_id': 'track_count', 'category': 'quarter'})
                .sort_values('quarter', ascending = True)
                .reset_index(drop=True)
                )

    return quartercount.to_dict(orient = 'records')



# Statistics for stream count and track count by country
def country_stats(df: pd.DataFrame):
    stats = (df.groupby('country')
        .agg(
            track_count  = ('track_id',    'nunique'),
            stream_count = ('stream_count', 'sum')
        )
        .reset_index()
        .sort_values('stream_count', ascending = False)
        .reset_index(drop = True)
    )
    return stats.to_dict(orient = 'records')
