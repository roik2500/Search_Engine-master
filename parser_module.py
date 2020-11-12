from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from document import Document
from re import findall


class Parse:
    def __init__(self):
        self.stop_words = stopwords.words('english')

    # Build a tokenize---> split by spaces
    def Tokenize(self, text):
        return text.split(' ')

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
        #text_tokens = word_tokenize(text)
        text_tokens = self.Tokenize(text)

        print(text_tokens)
       # text_tokens_without_stopwords = [w.lower() for w in text_tokens if w not in self.stop_words]

        text_tokens_without_stopwords = [w for w in text_tokens if w not in self.stop_words]
        print(text_tokens_without_stopwords)
        # self.hastag('#stayAtHomeTonighRoi')
        return text_tokens_without_stopwords

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
