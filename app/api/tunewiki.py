import urllib
import requests
import simplejson
import hashlib
import random

#API Keys
TUNEWIKI_API_KEY = ""
METROLYRICS_API_KEY = "1234567890123456789012345678901234567890"

class MetroLyrics(object):
    def __init__(self, api_key=None):
        self.lyrics_from_artist_song_endpoint = "http://api.metrolyrics.com/v1/search/artistsong/"
        self.full_lyrics_endpoint = "http://api.metrolyrics.com/v1/get/lyricdetails/"
        self.lyrics_from_song_endpoint = "http://api.metrolyrics.com/v1/search/lyrics/"
        self.api_key = api_key or METROLYRICS_API_KEY

    def get_search_results(self, song_name, artist_name=None):
        #Build the right request URL and query
        params = {'X-API-KEY': self.api_key}
        if artist_name:
            endpoint = self.lyrics_from_artist_song_endpoint
            params['title'] = song_name
            params['artist'] = artist_name
        else:
            endpoint = self.lyrics_from_song_endpoint
            params['find'] = song_name

        search_request_url = "%s?%s" % (endpoint, urllib.urlencode(params))

        response = requests.get(search_request_url)
        return simplejson.loads(response.text).get('items', [])

    def get_song_lyrics(self, song_name, artist_name, lyric_id):
        params = {'X-API-KEY': self.api_key}
        params['title'] = song_name
        params['artist'] = artist_name
        params['lyricid'] = lyric_id
        params['deviceid'] = hashlib.md5(str(random.random())).hexdigest() #random string

        lyrics_request_url = "%s?%s" % (self.full_lyrics_endpoint, urllib.urlencode(params))
        response = requests.get(lyrics_request_url)
        song_lyric_details_response = simplejson.loads(response.text)
        song_details = {}
        song_details['lyrics'] = song_lyric_details_response.get('song','')
        song_details['title'] = song_name
        song_details['artist'] = artist_name
        return song_details

    def get_song_lyrics_by_name(self, song_name, artist_name=None):
        song_lyrics = {}
        search_results = self.get_search_results(song_name, artist_name)
        #Fetch the first search result with lyrics and get those lyrics
        chosen_result = {}
        for result in search_results:
            lyrics_available = (result.get('content_status') == 1)
            if lyrics_available:
                chosen_result['song_name'] = result.get('title', '')
                chosen_result['artist_name'] = result.get('artist', '')
                chosen_result['lyric_id'] = result.get('lyricid', 0)
                break

        if chosen_result:
            song_lyrics = self.get_song_lyrics(**chosen_result)

        return song_lyrics

