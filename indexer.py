import math



class Indexer:
    def __init__(self):
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

        # this code for building the global table

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

    @staticmethod
    def CreatInvertedIndex(word_dict, idx, global_table):
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
