from flask import Flask, request, jsonify, send_from_directory 
from flask_cors import CORS
from flask_compress import Compress
import pandas as pd 
import os

df = pd.read_csv(r'D:\Data Science\Project cuối khóa 1 Mindx\spotify_data_processed.csv')

app = Flask(__name__)
CORS(app)
Compress(app)

# Serve dashboard at root URL
@app.route('/')
def dashboard():
    folder = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(folder, 'dashboard.html')

from data_processing import (get_all_track, 
                        filter_by_artist, 
                        filter_by_genre, 
                        filter_by_year, 
                        filter_by_label, 
                        filter_by_country,
                        filter_by_loudness, 
                        get_trackid, 
                        get_song,
                        suggest_song_names)

from data_handle import (create_new_track,
                    delete_track,
                    delete_track_by_song,
                    get_song_suggestions,
                    get_top_track,
                    get_bottom_track,
                    get_top_popularity,
                    top_genre,
                    top_year,
                    avg_pop,
                    month_track_count,
                    country_stats
                    )

from data_ultilize import (label_stream_count,
                    label_artist,
                    label_track_count
                    )

# Helper function to serialize DataFrame rows safely for JSON
def safe_dict(d: dict) -> dict:
    return {k: (None if pd.isna(v) else v) for k, v in d.items()}

# Paginated track data retrieval
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



# Return list of all tracks
@app.route('/api/summary')
def all():
    return jsonify(get_all_track(df))



# Multi-parameter query — genre, artist, year, label, country, loudness are optional => Filter by category
@app.route('/api/filter')
def filter_all():
    try:
        genre    = request.args.get('genre',    type = str)
        artist   = request.args.get('artist',   type = str)
        year     = request.args.get('year',     type = int)
        label    = request.args.get('label',    type = str)
        country  = request.args.get('country',  type = str)
        loudness = request.args.get('loudness', type = str)

        if 'year' in request.args and year is None:
            return jsonify({'error': 'Invalid year format, please provide a valid integer'}), 400 

        if not any([genre, artist, year, label, country, loudness]):
            return jsonify({'error': 'Please provide at least one filter parameter: genre, artist, year, label, country, loudness'}), 400


        result = []

        if genre:
            a = filter_by_genre(df, genre)
            if isinstance(a, dict) and 'error' in a:
                return jsonify(a), 404
            result = a  # assign value from a

        if year:
            b = filter_by_year(df, year)
            if isinstance(b, dict) and 'error' in b:
                return jsonify(b), 404
            result = [r for r in result if r in b] if result else b  # if result is empty, assign value from b

        if artist:
            c = filter_by_artist(df, artist)
            if isinstance(c, dict) and 'error' in c:
                return jsonify(c), 404
            result = [r for r in result if r in c] if result else c  # if result is empty, assign value from c

        if country:
            d = filter_by_country(df, country)
            if isinstance(d, dict) and 'error' in d:
                return jsonify(d), 404
            result = [r for r in result if r in d] if result else d  # if result is empty, assign value from d

        if label:
            e = filter_by_label(df, label)
            if isinstance(e, dict) and 'error' in e:
                return jsonify(e), 404
            result = [r for r in result if r in e] if result else e  # if result is empty, assign value from e

        if loudness:
            f = filter_by_loudness(df, loudness)
            if isinstance(f, dict) and 'error' in f:
                return jsonify(f), 404
            result = [r for r in result if r in f] if result else f


        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Search by track ID or song title
@app.route('/api/search')
def search():
    try:
        trackid = request.args.get('id',   type = str)
        song    = request.args.get('song', type = str)
        result  = []

        if not any([trackid, song]):
            return jsonify({'error': 'Please enter a track ID or song title'}), 400

        if trackid and song:
            return jsonify({'error': 'Please search by either track ID or song title, not both'}), 400

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



# Song suggestions for search and delete autocomplete
@app.route('/api/suggest')
def suggest():
    try:
        query = request.args.get('q', type = str) or request.args.get('song', type = str) or request.args.get('query', type = str) or ''
        limit = request.args.get('limit', default = 10, type = int)
        suggestions = get_song_suggestions(df, query, limit = limit)
        return jsonify(suggestions), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Add new track
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
    return jsonify({'message': 'Track added successfully', 'track': new_song}), 201



# Delete track by track ID or song title
@app.route('/api/remove', methods = ['DELETE'])
def remove():
    global df
    track_id  = request.args.get('id',   type = str)
    song_name = request.args.get('song', type = str) or request.args.get('name', type = str) or request.args.get('track_name', type = str)

    if not track_id and not song_name:
        return jsonify({'error': 'Please provide either a track ID (id) or song name (song)'}), 400

    try: 
        if track_id:
            remove_song = delete_track(df, track_id)
        else:
            remove_song = delete_track_by_song(df, song_name)

        if isinstance(remove_song, dict) and 'error' in remove_song:
            status_code = 400 if 'suggestions' in remove_song else 404
            return jsonify(remove_song), status_code

        df = remove_song
        return jsonify({'message': 'Track deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Top stream count
@app.route('/api/streamcount')
def top_stream():
    try:
        top = request.args.get('top', type = int)
        bot = request.args.get('bot', type = int)

        if top is None and bot is None:
            return jsonify({'error': 'Please specify either top or bot parameter'}), 400
        if top is not None and (top < 1 or top > len(df)):
            return jsonify({'error': 'Invalid top value, please select a number within range'}), 400
        if bot is not None and (bot < 1 or bot > len(df)):
            return jsonify({'error': 'Invalid bot value, please select a number within range'}), 400
        
        result = {}
        if top is not None:
            result['highest'] = get_top_track(df, top)
        if bot is not None:
            result['lowest'] = get_bottom_track(df, bot)
            
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Top popularity
@app.route('/api/popular')
def popularity():
    try:
        top = request.args.get('top', type = int)
        if top is None:
            return jsonify({'error': 'Please enter a number for top'}), 400
        if top is not None and (top < 1 or top > len(df)):
            return jsonify({'error': 'Invalid top value, please select a number within range'}), 400 

        result = {}
        if top is not None:
            result['most'] = get_top_popularity(df, top)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Calculate total stream count by genre, then rank
@app.route('/api/genrecountcrank')
def genre_assess():
    try:
        top = request.args.get('top', type = int)
        if top is not None and (top < 1 or top > len(df)):
            return jsonify({'error': 'Invalid top value, please select a number within range'}), 400

        result = top_genre(df, top)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


    
# Calculate total stream count by year, then rank
@app.route('/api/yearcountrank')
def year_assess():
    try:
        top = request.args.get('top', type = int)
        if top is not None and (top < 1 or top > len(df)):
            return jsonify({'error': 'Invalid top value, please select a number within range'}), 400

        result = top_year(df, top)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Calculate average popularity by genre, then categorize
@app.route('/api/poprank') 
def ranking():
    try:
        result = avg_pop(df)
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Number of tracks by quarter
@app.route('/api/quarterrank')
def quarter():
    try: 
        result = month_track_count(df)
        if isinstance(result, dict) and 'error' in result:
            return jsonify(result), 400

        return jsonify(result), 200
   
    except Exception as e:
        return jsonify({'error': str(e)}), 500




# Number of tracks per record label
@app.route('/api/label1')
def label_first():
    try:
        top = request.args.get('top', type = int)
        if top is not None and (top < 1 or top > len(df)):
            return jsonify({'error': 'Invalid top value, please select a number within range'}), 400

        result = label_track_count(df, top)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Total stream count per record label
@app.route('/api/label2')
def label_second():
    try:
        top = request.args.get('top', type = int)
        if top is not None and (top < 1 or top > len(df)):
            return jsonify({'error': 'Invalid top value, please select a number within range'}), 400     

        result = label_stream_count(top, df)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500




# Number of artists per record label
@app.route('/api/label3')
def label_third():
    try:
        top = request.args.get('top', type = int)
        if top is not None and (top < 1 or top > len(df)):
            return jsonify({'error': 'Invalid top value, please select a number within range'}), 400     

        result = label_artist(top, df)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Country statistics: track count and total stream count
@app.route('/api/countrystats')
def country_data():
    try:
        result = country_stats(df)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


df.to_csv(r'D:\Data Science\Project cuối khóa 1 Mindx\spotify_data_processed.csv', index = False)



if __name__ == '__main__':
    app.run(port=8888, debug=False)
