import math

from PostingbyTerm import PostingbyTerm
from memoryposting import MemoryPosting


class Indexer:
    def __init__(self):
        pass

    def add_new_doc(self, document, document_index, tweetID):
        """
        This function perform indexing process for a document list.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document:list of term (object term),int document_index (docId), int tweetid
        :return: -void
        """

        # Go over each term in the doc
        # this struct include a postingByTerm object
        postings = {}  ##key=term  value=(docID,tweetID,tf,tfi)
        max_term = 0  # number of maximum  word interfaces per doc

        for word in document:
            if word in postings.keys():
                postings[word].tfi += 1
            else:  # first doc of this word
                word.numOfDoc += 1
                postings[word] = PostingbyTerm(document_index, tweetID)
            max_term = max(max_term, postings[word].tfi)

        sigma = 0
        for word in postings.keys():
            postings[word].tfi = postings[word].tfi / max_term  ## tfij=fij/max{fj}
            sigma += postings[word].tfi ** 2
            word.postings.append(postings[word])

        if sigma != 0: sigma = 1 / math.sqrt(sigma)
        for word in postings.keys():
            postings[word].tfi *= sigma


    def CreatInvertedIndex(self, word_dict, idx):
        ##key:str name value: start,size,idfi=log(N/dfi)
        inverted_idx = {}
        N = idx + 1
        for word in list(word_dict.keys()):
            word = (word, word_dict.pop(word))
            if word[1].is_entity and word[1].numOfDoc < 2:
                inverted_idx[word[0]] = None
            else:
                inverted_idx[word[0]] = [0, math.log2(N / word[1].numOfDoc)]
        return inverted_idx
