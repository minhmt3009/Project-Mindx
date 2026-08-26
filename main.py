from flask import Flask, request, jsonify, send_from_directory 
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from data_processing import (get_all_track, 
                        filter_by_artist, 
                        filter_by_genre, 
                        filter_by_year, 
                        filter_by_label, 
                        filter_by_country, 
                        get_trackid, 
                        get_song
)

@app.route('/api/all')
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
        country= request.args.get('country',type = str)

        if 'year' in request.args and year is None:
            return jsonify({'error': 'Không hợp lệ, vui lòng nhập đúng định dạng'}), 400 

        if not any([genre, artist, year, label, country]):
            return jsonify({'error': 'Vui lòng nhập ít nhất 1 tham số: genre, artist, year'}), 400


        result = []

        if genre:
            a = filter_by_genre(genre)
            if isinstance(a, dict) and 'error' in a:
                return jsonify(a), 404
            result = a  # gắn giá trị từ a

        if year:
            b = filter_by_year(year)
            if isinstance(b, dict) and 'error' in b:
                return jsonify(b), 404
            result = [r for r in result if r in b] if result else b  # nếu result trống thì gắn giá trị từ b

        if artist:
            c = filter_by_artist(artist)
            if isinstance(c, dict) and 'error' in c:
                return jsonify(c), 404
            result = [r for r in result if r in c] if result else c  # nếu result trống thì gắn giá trị từ c

        if country:
            d = filter_by_country(country)
            if isinstance(d, dict) and 'error' in d:
                return jsonify(d), 404
            result = [r for r in result if r in d] if result else d  # nếu result trống thì gắn giá trị từ d

        if label:
            e = filter_by_label(label)
            if isinstance(e, dict) and 'error' in c:
                return jsonify(e), 404
            result = [r for r in result if r in e] if result else e  # nếu result trống thì gắn giá trị từ e


        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Tìm kiếm theo yêu cầu (track_id, tên bài hát)
@app.route('/api/search')
def search():
    try:
        trackid = request.args.get('id', type = str)
        song = request.args.get('song', type = str)
        result = []

        if not any ([trackid, song]):
            return jsonify({'error': 'Vui lòng nhập ID hoặc tên bài nhạc'}), 400

        if trackid:
            x = get_trackid(trackid)
            if isinstance(x, dict) and 'error' in x:
                return jsonify(x), 404
            result = x

        if song:
            y = get_song(song)
            if isinstance(y, dict) and 'error' in y:
                return jsonify(y), 404
            result = [r for r in result if r in y] if result else y 

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

        



if __name__ == '__main__':
    app.run(debug=True, port=8888)
