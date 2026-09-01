import pandas as pd
df = pd.read_csv(r'D:\Data Science\Project cuối khóa 1 Mindx\spotify_data_processed.csv')
from datetime import date

# Tự generate track id
def new_trackid(df: pd.DataFrame):
    if df.empty:
        return 'TRK-00001'

    numeric_parts = df["track_id"].str.replace("TRK-", "", regex=False).astype(int)
    next_number = numeric_parts.max() + 1
    
    return f"TRK-{next_number:05d}" 

default_values = {'album_name':'', 'duration_ms': 0, 'popularity': 50, 'stream_count':1000 }
required_values = ['track_name', 'artist_name', 'genre', 'country', 'label', 'loudness_category', 'release_date']


# Định dạng DATE
def parse_new_date(data: dict) -> pd.Timestamp:
    new_date = data.get('release_date')

    if not new_date:
        # Không nhập thì mặc định hôm nay
        return pd.Timestamp(date.today())

    try:
        return pd.to_datetime(new_date)
    except (ValueError, TypeError):
        return {'error': release_date}



# Tạo dữ liệu mới
def create_new_track (data: dict, df: pd.DataFrame) -> dict:
    missing = [f for f in required_values if not data.get(f)]
    if missing:
        return {'error': f'Thiếu trường bắt buộc: {missing}'}


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



# Xóa bài hát
def delete_track(df: pd.DataFrame, track_id: str):
    if track_id.lower() not in df['track_id'].str.lower().values:
        return {'error': 'Không tồn tại ID'}

    del_id = df.index[df['track_id'].str.lower() == track_id.lower()]
    if del_id.empty:
        return {'error': 'Không tìm thấy ID '}

    df = df.drop(index=del_id[0]).reset_index(drop=True)
    return df


default_cols = ['genre', 'country', 'label', 'track_id', 'track_name', 'artist_name', 'release_date', 'stream_count', 'popularity']

# Tìm top lượt stream cao và thấp nhất
def get_top_track(df: pd.DataFrame, top: int):
    highest = df.nlargest(top, 'stream_count')[default_cols].reset_index(drop=True)
    return highest.to_dict(orient = 'records')


def get_bottom_track(df: pd.DataFrame, bot: int):
    lowest = df.nsmallest(bot, 'stream_count')[default_cols].reset_index(drop=True)
    return lowest.to_dict(orient = 'records')


# Xếp hạng độ phổ biến
def get_top_popularity(df: pd.DataFrame, top: int):
    most = df.nlargest(top, 'popularity')[default_cols].reset_index(drop=True)
    return most.to_dict(orient = 'records')


# Tổng streamcount của genre
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



# Tổng streamcount theo năm
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



# Độ popularity trung bình theo genre => phân chia thành các loại: Very popular, popular, unpopular 
def classify_popularity(score):
    if score >= 70:
        return 'Very popular'
    elif score >= 40:
        return 'Popular'
    elif score <= 0:
        return {'error': 'Phải lớn hơn 0'}
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



# Số lượng bài theo từng quý của tất cả các năm
def classify_quarter(month: int):
    if 1 <= month <= 3:
        return 'Quý I'
    elif 4 <= month <= 6:
        return 'Quý II'
    elif 7 <= month <= 9:
        return 'Quý III'
    elif 10 <= month <= 12:
        return 'Quý IV'
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



# Thống kê stream count và số bài hát theo quốc gia
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






