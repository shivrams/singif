import requests
from lyric_parser import LyricParser
import urllib
import simplejson

GIPHY_API_KEY = "dc6zaTOxFJmzC"
class Giphy(object):
    def __init__(self, api_key=None):
        self.api_key = api_key or GIPHY_API_KEY
        self.search_by_keyword_endpoint = "http://api.giphy.com/v1/gifs/search"

    def get_gifs_by_keyword(self, keyword, offset=0, count=40, dont_parse=False):
        if not dont_parse:
            #Pick the most gif friendly keyword available
            keyword = LyricParser.get_keyword(keyword)

        params = {'api_key': self.api_key}
        params['q'] = keyword
        params['limit'] = count
        params['offset'] = offset
        search_request_url = "%s?%s" % (self.search_by_keyword_endpoint, urllib.urlencode(params))
        try:
            return simplejson.loads(requests.get(search_request_url, timeout=5).text)
        except Exception:
            return {}

    def get_recent_gifs_by_keyword(self, keyword, offset=0, count=40):
        pass

    def get_translated_gifs_by_keyword(self, keyword, offset=0, count=40):
        pass

    def get_gif_for_line(self, lyric_info, duration=None):
        chosen_gifs = []
        lyric_text = lyric_info['text']
        lyric_ts = lyric_info['ts']
        search_results = self.get_gifs_by_keyword(lyric_text, count=100)
        result_gifs = search_results.get('data', [])
        gif_count = search_results.get('pagination', {}).get('total_count', 0)
        if gif_count:
            max_chosen = 1
            if gif_count > 500:
                max_chosen = 2
            elif gif_count > 1000:
                max_chosen = 3
            elif gif_count == 0:
                max_chosen = 0

            #Choose based on duration
            #Ensure each gif has atleast 1 second playtime
            average_duration = 0
            while max_chosen > 1:
                average_duration = duration/max_chosen
                if average_duration < 1:
                    #Reduce the number of chosen gifs
                    max_chosen -= 1
                else:
                    break

            if max_chosen:
                #Weird hacky code to pick gifs with right timestamps
                for result_gif in result_gifs:
                    chosen_gif_url = result_gif.get('images', {}).get('original', {}).get('url', '')
                    if chosen_gif_url:
                        gif_info = {}
                        gif_info['url'] = chosen_gif_url
                        gif_info['ts'] = lyric_ts + (average_duration * len(chosen_gifs))
                        chosen_gifs.append(gif_info)
                        if len(chosen_gifs) >= max_chosen:
                            break

        return chosen_gifs
