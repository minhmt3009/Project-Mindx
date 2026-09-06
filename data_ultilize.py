import pandas as pd
df = pd.read_csv(r'D:\Data Science\Project cuối khóa 1 Mindx\spotify_data_processed.csv')


# Count number of tracks per record label
def label_track_count(df: pd.DataFrame, top: int = None):
    labelcounttrack = (df.groupby('label')['track_id']
            .nunique()
            .reset_index()
            .rename(columns={'track_id': 'track_count'})
            .sort_values('track_count', ascending = False)
            .reset_index(drop=True)
            )

    if top is not None:
        labelcounttrack = labelcounttrack.head(top)

    return labelcounttrack.to_dict(orient = 'records')




# Total stream count of tracks by record label
def label_stream_count(top: int = None, df: pd.DataFrame = None):
    labelstreamcount = (df.groupby('label')['stream_count']
            .sum()
            .reset_index()
            .sort_values('stream_count', ascending = False)
            .reset_index(drop=True)
            )

    if top is not None:
        labelstreamcount = labelstreamcount.nlargest(top, 'stream_count')

    return labelstreamcount.to_dict(orient = 'records')



# Count number of unique artists per record label (measure label prestige)
def label_artist(top: int = None, df: pd.DataFrame = None):
    artistcount = (df.groupby('label')['artist_name']
            .nunique()
            .reset_index()
            .rename(columns={'artist_name': 'artist_count'})
            .sort_values('artist_count', ascending = False)
            .reset_index(drop=True)
            )

    if top is not None:
        artistcount = artistcount.head(top)

    return artistcount.to_dict(orient = 'records')



# Get statistics on different categories by country
def country_details(df: pd.DataFrame, country: str, top: int = 5, years = None):
    if not country or not isinstance(country, str) or not country.strip():
        return {'error': 'Country name is required'}

    country_clean = country.strip()
    sub = df[df['country'].str.lower() == country_clean.lower()]
    
    if sub.empty:
        return {'error': f'No data found for country: {country_clean}'}

    all_years = sorted([int(y) for y in sub['release_year'].dropna().unique()])

    # Parse years if provided (can be int, list, or comma-separated string like "2019,2020,2021")
    selected_years = None
    if years is not None and str(years).strip() != '' and str(years).strip().lower() != 'all':
        if isinstance(years, (int, float)):
            selected_years = [int(years)]
        elif isinstance(years, str):
            parsed = []
            for item in years.split(','):
                item = item.strip()
                if item.isdigit():
                    parsed.append(int(item))
            if parsed:
                selected_years = parsed
        elif isinstance(years, (list, tuple)):
            selected_years = [int(y) for y in years if str(y).isdigit()]

    # 1. Overview
    overview = {
        'country': country_clean,
        'total_track': int(len(sub)),
        'total_stream': int(sub['stream_count'].sum()),
        'average_popularity': round(float(sub['popularity'].mean()), 1),
        'available_years': all_years
    }

    # 2. Most popular genres
    top_genre = (sub.groupby('genre')
        .agg(
            track_count=('track_id', 'count'),
            total_stream=('stream_count', 'sum')
        )
        .reset_index()
        .sort_values('track_count', ascending=False)
        .head(top)
        .to_dict(orient='records')
    )

    # 3. Top artists
    artists_numbers = (sub.groupby('artist_name')
        .agg(
            track_count=('track_id', 'nunique'),
            total_stream=('stream_count', 'sum')
        )
        .reset_index()
        .sort_values('track_count', ascending=False)
        .head(top)
        .to_dict(orient='records')
    )

    # 4. Top albums
    albums_numbers = (sub.groupby('album_name')
        .agg(
            track_count=('track_id', 'nunique'),
            total_stream=('stream_count', 'sum')
        )
        .reset_index()
        .sort_values('track_count', ascending=False)
        .head(top)
        .to_dict(orient='records')
    )

    # 5. Years of release (Combo chart data: bar for track_count, line for total_stream)
    year_target = sub
    if selected_years:
        matched = sub[sub['release_year'].isin(selected_years)]
        if not matched.empty:
            year_target = matched

    years_of_release = (year_target.groupby('release_year')
        .agg(
            track_count=('track_id', 'nunique'),
            total_stream=('stream_count', 'sum'),
            avg_popularity=('popularity', 'mean')
        )
        .reset_index()
        .sort_values('release_year', ascending=True)
    )
    years_of_release['avg_popularity'] = years_of_release['avg_popularity'].round(1)
    years_of_release_records = years_of_release.to_dict(orient='records')

    

    return {
        'overview': overview,
        'top_genre': top_genre,
        'artists_numbers': artists_numbers,
        'albums_numbers': albums_numbers,
        'years_of_release': years_of_release_records
    }