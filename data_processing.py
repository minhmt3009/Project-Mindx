import pandas as pd 
df = pd.read_csv(r'D:\Data Science\Project cuối khóa 1 Mindx\spotify_data_processed.csv')

# Danh sách toàn bộ bài hát
def get_all_track():
    return df.to_dict(orient = 'records')



# Lấy danh sách theo genre.
def filter_by_genre(genre):
    if genre.lower() not in df['genre'].str.lower().values:
        return {'error': 'Không tồn tại thể loại nhạc này trong danh sách'}
    result = df[df['genre'].str.lower() == genre.lower()]
    return result.to_dict(orient = 'records')


# Lấy danh sách theo nghệ sĩ
def filter_by_artist(artist):
    if artist.lower() not in df['artist_name'].str.lower().values:
        return {'error': 'Không có nghệ sĩ này'}
    result = df[df['artist_name'].str.lower() == artist.lower()]
    return result.to_dict(orient = 'records')


# Lấy danh sách theo năm
def filter_by_year(year):
    if year not in df['release_year'].values:
        return {'error': 'Năm không tồn tại trong dữ liệu, vui lòng chọn lại'}
    result = df[df['release_year'] == year]
    return result.to_dict(orient = 'records')


# Lấy danh sách theo hãng
def filter_by_label(label):
    if label.lower() not in df['label'].str.lower().values:
        return {'error': 'Năm không tồn tại trong dữ liệu, vui lòng nhập lại'}
    result = df[df['label'].str.lower() == label.lower()]
    return result.to_dict(orient = 'records')


# Lấy danh sách theo quốc gia
def filter_by_country(country):
    if country.lower() not in df['country'].str.lower().values:
        return {'error': 'Không có quốc gia trên'}
    result = df[df['country'].str.lower() == country.lower()]
    return result.to_dict(orient = 'records')


# Lấy bài hát qua track_id
def get_trackid(trackid):
    if trackid.lower() not in df['track_id'].str.lower().values:
        return {'error': 'Không tồn tại ID'}
    result = df[df['track_id'].str.lower() == trackid.lower()]
    return result.to_dict(orient = 'records')


# Lấy bài hát qua tên bài
def get_song(song):
    if song.lower() not in df['track_name'].str.lower().values:
        return {'error': 'Không có bài hát này'}
    result = df[df['track_name'].str.lower() == song.lower()]
    return result.to_dict(orient = 'records')



