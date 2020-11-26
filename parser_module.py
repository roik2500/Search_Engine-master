import math
import string
from nltk.corpus import stopwords
from Term import Term
from stemmer import Stemmer
import re
import json


class Parse:
    def __init__(self):
        self.idx = 0
        self.word_dict = {}
        self.stemmer = Stemmer()
        self.stop_words = [self.stemmer.stem_term(word) for word in stopwords.words('english')] + [
            'rt']  # TODO: get words from local file

        # boolean member that we get from the main
        # if True we will do a stemmer for each term and if False we not change the term
        self.UseStemmer = False

    def returnEntity(self):
        """
        This function return a list of words(entity) that appears at least in tow document
        and remove the words from dict
      :param -
      :return: list of all entity in the corpus
        """
        res = []
        entities = []
        entities += self.entity.keys()
        for word in entities:
            if len(self.entity[word].listOfDoc) >= 2:
                res.append(self.entity[word])
                # self.entity.pop(word)
        for e in res:
            self.word_dict[e.text.lower()] = e
        return res

    # helper function for nomberTostring-->return 3 digit after the point
    def round_down(self, n, decimals=0):
        multiplier = 10 ** decimals
        return math.floor(n * multiplier) / multiplier

    def isNumber(self, word):
        return '0' <= word[0] <= '9'

    def numberToString(self, num):
        if num < 1000:
            return str(num)
        elif 1000 <= num < 1000000:
            num = num / 1000
            num = self.round_down(num, 3)
            if num == int(num): num = int(num)
            s = str(num)
            return s + 'K'
        elif 1000000 <= num < 1000000000:
            num = num / 1000000
            num = self.round_down(num, 3)
            if num == int(num): num = int(num)
            s = str(num)
            return s + 'M'
        else:
            num = num / 1000000000
            num = self.round_down(num, 3)
            if num == int(num): num = int(num)
            s = str(num)
            return s + 'B'

    # This function is "cleaning" the word,removing a ,!@$&*... that appear in start/end of word
    def strip_punc(self, word):
        if word=='$':
            return word
        start = 0
        end = len(word) - 1
        while start < len(word) and word[start] in (string.punctuation + '\n\t'):
            if word[start] == '@' or word[start] == '#' or word[start] == '"': break
            start += 1
        while end >= 0 and word[end] in string.punctuation:
            if word[end]=='"' or word[end]=='$': break
            end -= 1
        return word[start:end + 1]

    # This function clean the text-->remove if not exsit in ascii table
    def removeEmojify(self, text):
        return text.encode('ascii', 'ignore').decode('ascii')

    # Build a tokenize---> split by spaces
    def Tokenize(self, text):  # TODO: add two more rules and names support
        text = self.removeEmojify(text)
        # word_list = [self.strip_punc(self.stemmer.stem_term(word)) for word in text.split()] # creating a list of split word after stemming
        word_list = []
        for word in text.split():
            if '"' in word:
                word_list.append(self.strip_punc(word))
            else:
                if self.UseStemmer == True:
                    word_list.append(self.strip_punc(self.stemmer.stem_term(word)))
                else:
                    word_list.append(self.strip_punc(word))
        output = []

        # find all the quotes in this doc
        # re.findall() find all quotes and return a list of quoets without " "
        quoets = re.findall(r'"(.*?)"', text)
        for q in quoets:
            qu = '"' + q + '"'
            output.append(self.add_to_dict(qu))

        # The main loop
        for i in range(len(word_list)):
            word = word_list[i]
            if not word:
                continue

            # find a entity
            if word_list[i] != '' and len(word) != len(word_list) and len(word_list[i]) > 1:
                entity = ''
                # collecting the words of entity to one word
                counter = i
                while counter < len(word_list) and len(word_list[counter]) > 1 and word_list[counter][
                    0].isupper() and not word_list[counter][1].isupper():
                    entity += word_list[counter] + ' '
                    counter += 1
                entity = entity[:-1]

                # list_of_entity.append(word[1:])
                # if entity == '': continue

                if entity != '' and len(entity.split()) > 1:  # update the dict of entities
                    if entity not in self.word_dict.keys():
                        t = Term(entity)
                        t.listOfDoc.add(self.idx)
                        self.word_dict[entity.lower()] = t
                        output.append(t)
                    else:
                        self.word_dict[entity.lower()].listOfDoc.add(self.idx)
                        output.append(self.word_dict[entity.lower()])

                # if entity in self.entity.keys():
                #     self.entity[entity].listOfDoc.add(self.idx) #we will check if len(listofdoc)>=2 after the pares all of corpus
                # else:
                #     t = Term(entity)
                #     t.listOfDoc.add(self.idx)
                #     self.entity[entity] = t #key=string entity   value=Term of entity
                # entity = ''
            # if word == word_list[-1]:continue

            if self.isNumber(word):
                try:  # here we are checking the text by the roles of parse
                    if word[-1] == '%' or word_list[i + 1] == 'percent' or word_list[i + 1] == 'percentag':
                        if word[-1] != '%':
                            i += 1
                            word = word + '%'


                    if word_list[i+1] == '$':
                        w_1 = word+word_list[i+1]
                        w_2 = word+' '+word_list[i+1]
                        output.append(self.add_to_dict(w_1))
                        output.append(self.add_to_dict(w_2))


                    # check if the number is acctualy sperate to 2 word: 35 3/5
                    elif self.isNumber(word) and self.isNumber(word_list[i + 1]) and word_list[i + 1].__contains__('/'):
                        word += ' ' + word_list[i + 1]
                        output.append(self.add_to_dict(word))
                    # cases of Thousand=K    Millio=M    Billio=B--->the function numberToString do it
                    elif word_list[i + 1] == 'Thousand' or word_list[i + 1] == 'thousand':
                        i += 1
                        word = self.numberToString(float(word) * 1000)
                    elif word_list[i + 1] == 'Million' or word_list[i + 1] == 'million':
                        i += 1
                        word = self.numberToString(float(word) * 1000000)
                    elif word_list[i + 1] == 'Billion' or word_list[i + 1] == 'billion':
                        i += 1
                        word = self.numberToString(float(word) * 1000000000)
                    else:
                        word = self.numberToString(float(word))
                    output.append(self.add_to_dict(word))
                except:
                    output.append(self.add_to_dict(word))
            # hastag
            elif word[0] == '#':
                for word in self.hastag(word):
                    output.append(self.add_to_dict(word))
            # URL
            elif word[0:4] == "http":
                for word in self.URL(word):
                    output.append(self.add_to_dict(word))
            # Tag
            elif word[0] == '@':
                output.append(self.add_to_dict(word))
            else:
                output.append(self.add_to_dict(word))
        return output

    def add_to_dict(self, word):
        low_case = word.lower()
        if low_case in self.word_dict.keys():
            self.word_dict[low_case].numOfInterfaces += 1
            if word == low_case:
                self.word_dict[low_case].text = low_case
        else:
            self.word_dict[low_case] = Term(word)
        return self.word_dict[low_case]

    # #stayAtHome--->['#stayAtHome', 'stay', 'At',Home]
    def hastag(self, term):
        res = [term]
        start = 1
        for i in range(2, len(term)):
            if term[i].isupper():
                res.append(term[start:i])
                start = i
        res.append(term[start:])
        return res

    def URL(self, text):
        return [v for v in re.split('[://]|[/?]|[/]|[=]', text) if v]

    def extendURLs(self, document):
        url_map = json.loads(document[3])
        url_indices = json.loads(document[4])
        full_text = document[2]
        for index in url_indices:
            full_text = full_text[:index[0]] + url_map[full_text[index[0]:index[1]]] + full_text[index[1]:]
        document[2] = full_text


    def parse_sentence(self, text):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:
        """

        text_tokens = [token for token in self.Tokenize(text) if token.text.lower() not in self.stop_words]
        return text_tokens

    def parse_doc(self, doc_as_list, idx=None):
        """
        This function takes a tweet document as list and break it into different fields
        :param doc_as_list: list re-preseting the tweet.
        :return: Document object with corresponding fields.
        """
        # self.extendURLs(doc_as_list)

        self.idx = idx

        out = self.parse_sentence(doc_as_list[2])

        # out+=self.parse_sentence(doc_as_list[3])
        ##### for check ######

        # print(out)

        # print(self.word_dict)
        # print(self.entity['Roi Kremer'].numOfDoc)

        ##### for check #######
        return out

        # tweet_id = doc_as_list[0]
        # tweet_date = doc_as_list[1]
        # full_text = doc_as_list[2]
        # url = doc_as_list[3]
        # retweet_text = doc_as_list[4]
        # retweet_url = doc_as_list[5]
        # quote_text = doc_as_list[6]
        # quote_url = doc_as_list[7]
        # term_dict = {}
        #
        # tokenized_text = self.parse_sentence(full_text)
        # #tokenized_text = self.parse_sentence("@roi i go to Roi Kremer 10 3/7 #mom")
        # #print(tokenized_text)
        #
        # doc_length = len(tokenized_text)  # after text operations.
        # checkterms=set()
        # for term in tokenized_text: # tf
        #     if term not in checkterms:
        #         term.numOdDoc += 1
        #         checkterms.add(term)
        #     if term not in term_dict.keys():
        #         term_dict[term] = 1
        #     else:
        #         term_dict[term] += 1
        # document = Document(tweet_id, tweet_date, full_text, url, retweet_text, retweet_url, quote_text,
        #                     quote_url, term_dict, doc_length)
        # return document
