import abc
import time
import json
from os import walk
from ast import literal_eval

class WordCount(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_word_count(self, sentence: str):
        words={}
        for w in sentence.split():
            if w not in words:
                words[w] = 0
            words[w] += 1

        return words

    @abc.abstractmethod
    def get_tweets_word_count_by_file(self, folder_path: str):
        raise NotImplementedError


class SimpleWordCount(WordCount):
    def get_tweets_word_count_by_file(self, folder_path: str):
        words_count={}
        (tweets_path, tweets_directories, tweets_files) = next(walk(folder_path))

        for tweets in tweets_files:
            words_count[tweets]={}

            with open(tweets_path + tweets) as f:
                for raw in f.readlines():
                    line = literal_eval(raw).decode('utf-8')
                    words_count[tweets] = super().get_word_count(line)

        return words_count
    

simple = SimpleWordCount()

simple_start = time.time()
result = simple.get_tweets_word_count_by_file('tweets/')
simple_duration = time.time() - simple_start

print(json.dumps(result, indent = 4))

print(f'Simple Count duration: {simple_duration}')