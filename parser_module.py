import math

from nltk.corpus import stopwords
from document import Document
from Term import Term
from nltk.stem import PorterStemmer
from stemmer import Stemmer
import re

class Parse:
    def __init__(self):
        self.stop_words = stopwords.words('english')
        self.word_dict = {}
        self.stemmer = Stemmer()

# helper function for nomberTostring-->return 3 digit after the point
    def round_down(self,n, decimals=0):
        multiplier = 10 ** decimals
        return math.floor(n * multiplier) / multiplier

    def nomberTostring(self, num):
        if num < 1000:
            return str(num)
        elif 1000 <= num < 1000000:
            num = num / 1000
            num = self.round_down(num, 3)
            if num == int(num): num=int(num)
            s = str(num)
            return s+'K'
        elif 1000000 <= num < 1000000000:
            num=num/1000000
            num = self.round_down(num, 3)
            if num == int(num): num=int(num)
            s = str(num)
            return s+'M'
        else:
            num=num/1000000000
            num = self.round_down(num, 3)
            if num == int(num): num=int(num)
            s=str(num)
            return s+'B'

    # Build a tokenize---> split by spaces
    def Tokenize(self, text):
        word_list = [self.stemmer.stem_term(word) for word in text.split(' ') if word not in self.stop_words]

        # return [self.add_to_dict(word) for word in word_list]
        return word_list

    def add_to_dict(self, word):
        low_case = word.lower()
        if low_case in self.word_dict.keys():
            if word == low_case:
                self.word_dict[low_case].text = low_case

        else:
            self.word_dict[low_case] = Term(word)
        return self.word_dict[low_case]

    # #stayAtHome--->['#stayAtHome', 'stay', 'At',Home]
    def hastag(self, term):
        res = [term]
        if term[0] == '#':
            start = 1
            for i in range(2, len(term)):
                if term[i].isupper():
                    res.append(term[start:i])
                    start = i
            res.append(term[start:])
        return res

    def URL(self,text):
        if text[0:5] == "https":
            return [v for v in re.split('[://]|[/?]|[/]|[=]',text) if v]
        else : return [text]



    # @roi
    def tag(self, text):
        res = []
        start = 0
        for i in range(len(text)):
            if text[i] == '@':
                start = i
            if text[i] == ' ' and start != 0:
                if text[i - 1] == ':':
                    res.append(text[start:i - 1])
                else:
                    res.append(text[start:i + 1])
                break
        print(res)

    def parse_sentence(self, text):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:
        """
        text_tokens = self.Tokenize(text)

        print(text_tokens)
        # self.hastag('#stayAtHomeTonighRoi')
        return text_tokens

    def parse_doc(self, doc_as_list):
        """
        This function takes a tweet document as list and break it into different fields
        :param doc_as_list: list re-preseting the tweet.
        :return: Document object with corresponding fields.
        """
        tweet_id = doc_as_list[0]
        tweet_date = doc_as_list[1]
        full_text = doc_as_list[2]
        url = doc_as_list[3]
        retweet_text = doc_as_list[4]
        retweet_url = doc_as_list[5]
        quote_text = doc_as_list[6]
        quote_url = doc_as_list[7]
        term_dict = {}
        tokenized_text = self.parse_sentence(full_text)

        doc_length = len(tokenized_text)  # after text operations.

        for term in tokenized_text:  # tf
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1
        print(self.tag(full_text))
        document = Document(tweet_id, tweet_date, full_text, url, retweet_text, retweet_url, quote_text,
                            quote_url, term_dict, doc_length)
        return document
