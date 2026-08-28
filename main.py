from flask import Flask, request, jsonify, send_from_directory 
from flask_cors import CORS
import pandas as pd 
df = pd.read_csv(r'D:\Data Science\Project cuối khóa 1 Mindx\spotify_data_processed.csv')

app = Flask(__name__)
CORS(app)

from data_processing import (get_all_track, 
                        filter_by_artist, 
                        filter_by_genre, 
                        filter_by_year, 
                        filter_by_label, 
                        filter_by_country,
                        filter_by_loudness, 
                        get_trackid, 
                        get_song)

from data_handle import (create_new_track,
                    delete_track,
                    get_top_track,
                    get_bottom_track,
                    get_top_popularity,
                    top_genre,
                    top_year,
                    avg_pop,
                    classify
                    )



# Chia page
@app.route('/api/all')
def all_data():
    try:
        page     = request.args.get('page',     default=1,    type=int)
        per_page = request.args.get('per_page', default=50,   type=int)

        start = (page - 1) * per_page
        end   = start + per_page

        chunk   = df.iloc[start:end].copy()
        records = [safe_dict(r) for r in chunk.to_dict(orient='records')]

        return jsonify({
            'total':    len(df),
            'page':     page,
            'per_page': per_page,
            'data':     records
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Trả danh sách toàn bộ bài hát
@app.route('/api/summary')
def all():
    return jsonify(get_all_track())



# Query kết hợp nhiều tham số — genre, artist, year đều optional => Lọc theo category
@app.route('/api/filter')
def filter_all():
    try:
        genre  = request.args.get('genre',  type = str)
        artist = request.args.get('artist', type = str)
        year   = request.args.get('year',   type = int)
        label  = request.args.get('label',  type = str)
        country = request.args.get('country',type = str)
        loudness = request.args.get('country',type = str)

        if 'year' in request.args and year is None:
            return jsonify({'error': 'Không hợp lệ, vui lòng nhập đúng định dạng'}), 400 

        if not any([genre, artist, year, label, country, loudness]):
            return jsonify({'error': 'Vui lòng nhập ít nhất 1 tham số: genre, artist, year'}), 400


        result = []

        if genre:
            a = filter_by_genre(df, genre)
            if isinstance(a, dict) and 'error' in a:
                return jsonify(a), 404
            result = a  # gắn giá trị từ a

        if year:
            b = filter_by_year(df, year)
            if isinstance(b, dict) and 'error' in b:
                return jsonify(b), 404
            result = [r for r in result if r in b] if result else b  # nếu result trống thì gắn giá trị từ b

        if artist:
            c = filter_by_artist(df, artist)
            if isinstance(c, dict) and 'error' in c:
                return jsonify(c), 404
            result = [r for r in result if r in c] if result else c  # nếu result trống thì gắn giá trị từ c

        if country:
            d = filter_by_country(df, country)
            if isinstance(d, dict) and 'error' in d:
                return jsonify(d), 404
            result = [r for r in result if r in d] if result else d  # nếu result trống thì gắn giá trị từ d

        if label:
            e = filter_by_label(df, label)
            if isinstance(e, dict) and 'error' in e:
                return jsonify(e), 404
            result = [r for r in result if r in e] if result else e  # nếu result trống thì gắn giá trị từ e

        if loudness:
            f = filter_by_loudness(df, loudness)
            if isinstance(f, dict) and 'error' in f:
                return jsonify(f), 404
            result = [r for r in result if r in f] if result else f


        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Tìm kiếm theo yêu cầu (track_id, tên bài hát)
@app.route('/api/search')
def search():
    try:
        trackid = request.args.get('id',   type = str)
        song    = request.args.get('song', type = str)
        result  = []

        if not any([trackid, song]):
            return jsonify({'error': 'Vui lòng nhập ID hoặc tên bài nhạc'}), 400

        if trackid and song:
            return jsonify({'error': 'Chỉ được tìm bằng ID hoặc tên bài, không được dùng cả hai'}), 400

        if trackid:
            x = get_trackid(df, trackid)
            if isinstance(x, dict) and 'error' in x:
                return jsonify(x), 404
            result = x

        if song:
            y = get_song(df, song)
            if isinstance(y, dict) and 'error' in y:
                return jsonify(y), 404
            result = y

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Thêm mới
@app.route('/api/new', methods = ['POST'])
def add():
    global df
    data = request.get_json()

    try:
        new_song = create_new_track(data, df)
        if isinstance(new_song, dict) and 'error' in new_song:
            return jsonify(new_song), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    df = pd.concat([df, pd.DataFrame([new_song])], ignore_index = True)
    return jsonify({'message': 'Đã thêm mới thành công'}), 201



# Xóa
@app.route('/api/remove', methods = ['DELETE'])
def remove():
    global df
    track_id = request.args.get('id',   type = str)
    try: 
        remove_song = delete_track(df, track_id)
        if isinstance(remove_song, dict) and 'error' in remove_song:
            return jsonify(remove_song), 400

        return jsonify({'message': 'Đã xóa thành công'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Top lượt stream
@app.route('/api/streamcount')
def top_stream():
    try:
        top = request.args.get('top', type = int)
        bot = request.args.get('bot', type = int)

        if top is None and bot is None:
            return jsonify({'error': 'Vui lòng chọn một'})
        if top is not None and (top < 1 or top > len(df)):
            return jsonify({'error': 'Vui lòng chọn lại số'}), 400
        if bot is not None and (bot < 1 or bot > len(df)):
            return jsonify({'error': 'Vui lòng chọn lại số'}), 400
        
        result = {}
        if top is not None:
            result['highest'] = get_top_track(df, top)
        if bot is not None:
            result['lowest'] = get_bottom_track(df, bot)
            
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Top độ phổ biến
@app.route('/api/popular')
def popularity():
    try:
        top = request.args.get('top', type = int)
        if top is None:
            return jsonify({'error': 'Vui lòng nhập số'}), 400
        if top is not None and (top < 1 or top > len(df)):
            return jsonify({'error': 'Vui lòng chọn lại số'}), 400 

        result = {}
        if top is not None:
            result['most'] = get_top_popularity(df, top)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Tính tổng streamcount theo genre, sau đó xếp hạng
@app.route('/api/genrecountcrank')
def genre_assess():
    try:
        top = request.args.get('top', type = int)
        if top is not None and (top < 1 or top > len(df)):
            return jsonify({'error': 'Vui lòng chọn lại số'}), 400

        result = top_genre(df, top)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


    
# Tính tổng streamcount theo năm, sau đó xếp hạng
@app.route('/api/yearcountrank')
def year_assess():
    try:
        top = request.args.get('top', type = int)
        if top is not None and (top < 1 or top > len(df)):
            return jsonify({'error': 'Vui lòng chọn lại số'}), 400

        result = top_year(df, top)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Tính popularity trung bình của genre, sau đó phân loại
@app.route('/api/poprank') 
def ranking():
    try:
        result = avg_pop(df)
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
   



if __name__ == '__main__':
    app.run(debug=True, port=8888)
