import math
import utils
from posting_by_term import PostingByTerm


class Indexer:
    # __slots__ = ['global_table']

    def __init__(self):
        # self.global_table = {}
        pass

    @staticmethod
    def add_new_doc(document, document_index, tweet_id):
        """
        This function perform indexing process for a document list.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param tweet_id:
        :param document_index:
        :param document:list of term (object term),int document_index (docId), int tweet_id
        :return: -void
        """

        # Go over each term in the doc
        # this struct include a postingByTerm object
        postings = {}  # key=term  value=(docID,tweetID,tf,tfi)
        max_term = 0  # number of maximum  word interfaces per doc
        # self.addTOGlobalMethod(document)
        for word in document:
            if word in postings.keys():
                postings[word].tfi += 1
            else:  # first doc of this word
                word.numOfDoc += 1
                postings[word] = PostingByTerm(document_index, tweet_id)
            max_term = max(max_term, postings[word].tfi)

        sigma = 0
        for word in postings.keys():
            postings[word].tfi = postings[word].tfi / max_term  # tf_ij=f_ij/max{fj}
            sigma += postings[word].tfi ** 2
            word.postings.append(postings[word])

        if sigma != 0:
            sigma = 1 / math.sqrt(sigma)
        for word in postings.keys():
            postings[word].tfi *= sigma

    # def addTOGlobalMethod(self, Document):
    #     """
    #     This function are updating the global table
    #     The function taking two words any time from list and calculate the colorization between them
    #     :param Document: list of term (object term)
    #     :return: void
    #     """
    #     Document = [word.text.lower() for word in Document]
    #     for word_1 in Document:
    #         if word_1 not in self.global_table.keys():
    #             self.global_table[word_1] = {}
    #         for word_2 in Document:
    #             # if word_1 == word_2: continue
    #             if word_2 not in self.global_table[word_1].keys():
    #                 self.global_table[word_1][word_2] = 0
    #             self.global_table[word_1][word_2] += 1
    
    # def Creat_and_load_global_table(self):
    #     top_global = {}
    #     for word_1 in self.global_table.keys():
    #         top = []
    #         for word_2 in self.global_table[word_1].keys():
    #             s = self.global_table[word_1][word_2] / (
    #                     self.global_table[word_1][word_1] + self.global_table[word_2][word_2] -
    #                     self.global_table[word_1][word_2])
    #             if len(top) < 10:
    #                 top.append((word_2, s))
    #                 top.sort(key=lambda score: score[1])
    #             elif s > top[0][1]:
    #                 top[0] = (word_2, s)
    #                 top.sort(key=lambda score: score[1])
    #         top_global[word_1] = top
    #     utils.save_obj(top_global, 'global_table')

    @staticmethod
    def CreatInvertedIndex(word_dict, idx):
        global_table = utils.load_obj('global_table')
        # key:str name value: start,size,idf_i=log(N/dfi)
        inverted_idx = {}
        n = idx + 1
        for word in list(word_dict.keys()):
            word = (word, word_dict.pop(word))
            if word[1].numOfDoc == 0:
                inverted_idx[word[0]] = None
            elif word[1].is_entity and word[1].numOfDoc < 2:
                inverted_idx[word[0]] = None
            else:
                inverted_idx[word[0]] = [0, math.log2(n / word[1].numOfDoc), global_table[word[0]]]
        return inverted_idx
