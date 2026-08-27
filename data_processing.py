import pandas as pd 
df = pd.read_csv(r'D:\Data Science\Project cuối khóa 1 Mindx\spotify_data_processed.csv')

# Danh sách toàn bộ bài hát
def get_all_track(df: pd.DataFrame):
    return df.to_dict(orient = 'records')



# Lấy danh sách theo genre.
def filter_by_genre(df: pd.DataFrame, genre):
    if genre.lower() not in df['genre'].str.lower().values:
        return {'error': 'Không tồn tại thể loại nhạc này trong danh sách'}
    result = df[df['genre'].str.lower() == genre.lower()]
    return result.to_dict(orient = 'records')


# Lấy danh sách theo nghệ sĩ
def filter_by_artist(df: pd.DataFrame, artist):
    if artist.lower() not in df['artist_name'].str.lower().values:
        return {'error': 'Không có nghệ sĩ này'}
    result = df[df['artist_name'].str.lower() == artist.lower()]
    return result.to_dict(orient = 'records')


# Lấy danh sách theo năm
def filter_by_year(df: pd.DataFrame, year):
    if year not in df['release_year'].values:
        return {'error': 'Năm không tồn tại trong dữ liệu, vui lòng chọn lại'}
    result = df[df['release_year'] == year]
    return result.to_dict(orient = 'records')


# Lấy danh sách theo hãng
def filter_by_label(df: pd.DataFrame, label):
    if label.lower() not in df['label'].str.lower().values:
        return {'error': 'Năm không tồn tại trong dữ liệu, vui lòng nhập lại'}
    result = df[df['label'].str.lower() == label.lower()]
    return result.to_dict(orient = 'records')


# Lấy danh sách theo quốc gia
def filter_by_country(df: pd.DataFrame, country):
    if country.lower() not in df['country'].str.lower().values:
        return {'error': 'Không có quốc gia trên'}
    result = df[df['country'].str.lower() == country.lower()]
    return result.to_dict(orient = 'records')


# Lấy danh sách theo độ ồn
def filter_by_loudness(df: pd.DataFrame, loudness):
    if loudness.lower() not in df['loudness_category'].str.lower().values:
        return {'error': 'Không tồn tại'}
    result = df[df['loudness_category'].str.lower() == loudness.lower()]
    return result.to_dict(orient = 'records')


# Lấy bài hát qua track_id
def get_trackid(df: pd.DataFrame, trackid):
    if trackid.lower() not in df['track_id'].str.lower().values:
        return {'error': 'Không tồn tại ID'}
    result = df[df['track_id'].str.lower() == trackid.lower()]
    return result.to_dict(orient = 'records')


# Lấy bài hát qua tên bài
def get_song(df: pd.DataFrame, song):
    if song.lower() not in df['track_name'].str.lower().values:
        return {'error': 'Không có bài hát này'}
    result = df[df['track_name'].str.lower() == song.lower()]
    return result.to_dict(orient = 'records')






