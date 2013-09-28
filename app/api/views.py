from flask import Response, Blueprint
from tunewiki import MetroLyrics
from lyric_parser import LyricParser
from giphy import Giphy
from copy import deepcopy
import simplejson
from flask import request

sample_response = {'status': 200, 'gifs': [{'url': 'http://media.giphy.com/media/fiMcQZFenlgFa/giphy.gif', 'loops': 8, 'style': 'center', 'ts': 0}, {'url': 'http://media.giphy.com/media/Jztx4VDq2wJBS/giphy.gif', 'loops': 4, 'style': 'center', 'ts': 14}, {'url': 'http://media.giphy.com/media/cr5u0ZEbQpVPG/giphy.gif', 'loops': -1, 'style': 'tile', 'ts': 21}], 'lines': [{'text': 'oh yeah', 'ts': 8}, {'text': 'such sweet lyrics', 'ts': 14}, {'text': 'time to gif it', 'ts': 21}], 'meta': {'original_url': 'https://www.youtube.com/watch?v=hroUeu4IvpE', 'id': 'hroUeu4IvpE', 'embed_type': 'youtube', 'internal_id': '12151', 'title': 'blah', 'artist': 'WASTE', 'length': 27}, 'mesg': 'success'}

mod = Blueprint('api', __name__)

@mod.route('/ping')
def ping():
    return 'pong!'

@mod.route('/api/v1/singif')
def singif_api():
    provided_song_name = request.args.get("song_name", "")
    if not provided_song_name:
        json_response = simplejson.dumps(sample_response)
    else:
        song_response = {}
        song_gifs = []
        song_lyrics = []
        lyric_engine = MetroLyrics()
        gif_engine = Giphy()

        song_lyrics_meta = lyric_engine.get_song_lyrics_by_name(provided_song_name)
        song_meta = deepcopy(song_lyrics_meta)
        song_meta['original_url'] = "https://www.youtube.com/watch?v=hroUeu4IvpE"
        song_meta['embed_type'] = 'youtube'
        song_meta['id'] = 'hroUeu4IvpE'
        song_meta['internal_id'] = 'test'
        full_song_lyrics = song_lyrics_meta.get('lyrics')
        individual_lyrics = LyricParser.get_lyric_lines(full_song_lyrics)
        current_timestamp = 0
        for lyric in individual_lyrics:
            lyric_duration = LyricParser.estimate_duration(lyric)
            lyric_info = {}
            lyric_info['text'] = lyric
            lyric_info['ts'] = current_timestamp + lyric_duration
            current_timestamp += lyric_duration
            song_lyrics.append(lyric_info)
            lyric_gifs = gif_engine.get_gif_for_line(lyric_info, duration=lyric_duration)
            if lyric_gifs:
                song_gifs.extend(lyric_gifs)

        song_response['gifs'] = song_gifs
        song_response['lines'] = song_lyrics
        song_response['meta'] = song_meta

        song_response['status'] = 200
        json_response = simplejson.dumps(song_response)

    resp = Response(json_response, status=200, mimetype='application/json')
    resp.headers['X-Creator'] =  "W.A.S.T.E"
    resp.headers['Access-Control-Allow-Origin'] = "*"
    return resp

