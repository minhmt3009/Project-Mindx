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