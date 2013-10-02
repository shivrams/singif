import re
import random

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
    def tokenize(cls, lyric):
        lyric = lyric.lower()
        lyric = re.sub("[^a-z ]","",lyric)
        lyric_words = lyric.split()
        return lyric_words


    @classmethod
    def get_keyword(cls, lyric):
        tokenized_lyric = cls.tokenize(lyric)
        stop_words = set(['all', 'just', 'howll', 'being', 'able', 'over', 'both', 'wholl', 'isnt', 'through', 'yourselves', 'its', 'before', 'aint', 'also', 'herself', 'had', 'should', 'to', 'only', 'under', 'ours', 'has', 'might', 'do', 'them', 'his', 'get', 'very', 'youll', 'cannot', 'every', 'they', 'werent', 'not', 'during', 'now', 'him', 'nor', 'wont', 'like', 'did', 'mightnt', 'shant', 'theyre', 'this', 'whatd', 'she', 'each', 'further', 'wouldve', 'where', 'few', 'shell', 'shed', 'because', 'says', 'often', 'doing', 'theyd', 'some', 'whens', 'whys', 'likely', 'are', 'cant', 'our', 'ourselves', 'out', 'what', 'said', 'for', 'since', 'while', 'yet', 'does', 'above', 'between', 'got', 'neither', 'ever', 'across', 't', 'be', 'we', 'who', 'were', 'however', 'here', 'didnt', 'whenll', 'hers', 'by', 'on', 'about', 'would', 'wouldnt', 'mightve', 'of', 'could', 'hes', 'against', 's', 'must', 'arent', 'youve', 'let', 'theres', 'or', 'thats', 'among', 'own', 'whats', 'dont', 'into', 'youd', 'yourself', 'down', 'doesnt', 'least', 'twas', 'couldnt', 'your', 'from', 'her', 'their', 'id', 'there', 'been', 'whos', 'hed', 'whom', 'too', 'whod', 'themselves', 'was', 'until', 'more', 'wants', 'himself', 'that', 'but', 'else', 'don', 'mustnt', 'with', 'than', 'those', 'he', 'me', 'myself', 'theyve', 'these', 'up', 'us', 'will', 'below', 'can', 'theirs', 'whend', 'whyd', 'my', 'ill', 'say', 'shes', 'and', 'ive', 'thatll', 'then', 'almost', 'wed', 'is', 'whyll', 'am', 'it', 'an', 'dear', 'as', 'itself', 'im', 'at', 'have', 'in', 'any', 'if', 'again', 'hasnt', 'theyll', 'no', 'rather', 'when', 'same', 'tis', 'how', 'other', 'which', 'you', 'either', 'shouldnt', 'may', 'whered', 'shouldve', 'after', 'most', 'couldve', 'wherell', 'mustve', 'such', 'wasnt', 'why', 'wheres', 'a', 'hows', 'off', 'i', 'youre', 'well', 'yours', 'so', 'howd', 'the', 'having', 'once'])
        good_words = []
        for word in tokenized_lyric:
            if word not in stop_words:
                good_words.append(word)

        return random.choice(good_words)

    @classmethod
    def estimate_duration(cls, lyric):
        if not lyric:
            duration = 2

        #estimate at 1 second for every 10 characters
        duration = len(lyric)/10

        if duration == 0:
            duration = 1

        return duration
