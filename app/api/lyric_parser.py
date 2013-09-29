import re

class LyricParser(object):
    @classmethod
    def get_lyric_lines(cls, full_lyrics):
        if not full_lyrics:
            return []

        #Guess a delimiter for the lyric body
        delimiter = None
        if '\n' in full_lyrics:
            delimiter = '\n'

        elif '..' in full_lyrics:
            delimiter = '..'

        elif '.' in full_lyrics:
            delimiter = '.'

        elif ',' in full_lyrics:
            return full_lyrics.split(',')

        if delimiter:
            lines = full_lyrics.split(delimiter)
        else:
            lines = re.split("[^a-zA-Z0-9 ]", full_lyrics)

        final_lines = []
        for line in lines:
            if line:
                final_lines.append(line)

        return final_lines

    @classmethod
    def get_keyword(cls, lyric):
        return lyric

    @classmethod
    def estimate_duration(cls, lyric):
        if not lyric:
            duration = 2

        #estimate at 1 second for every 10 characters
        duration = len(lyric)/10

        return duration
