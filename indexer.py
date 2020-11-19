from PostingbyTerm import PostingbyTerm


class Indexer:
    def __init__(self, config):
        self.inverted_idx = {}  ## key=term    value=( numOfDoc , TotalnumberInCorpus ,pointerToPosting )

        ##key=term   value=list postingbyterm
        self.postingDict = {}

        self.config = config
        self.numberOfDocuments = 0  #N

    def add_new_doc(self, document, document_index, tweetID):
        """
        This function perform indexing process for a document list.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """
        # self.numberOfDocuments += 1
        # document_dictionary = document.term_doc_dictionary
        # Go over each term in the doc

        #this structur include a postingbyTerm object
        postings = {}

        max_term = 0  # number of maximum interfaces per doc
        for word in document:
            if word in postings.keys():
                postings[word].tfi += 1
            else:
                word.numOdDoc += 1
                postings[word] = PostingbyTerm(document_index, tweetID)
            max_term = max(max_term, postings[word].tfi)

        for word in postings.keys():
            postings[word].tfi = postings[word].tfi/max_term    ## tfij=fij/max{fj}
            if word in self.postingDict.keys():
                self.postingDict[word].append(postings[word])
            else:
                self.postingDict[word] = [postings[word]]




        # for term in document_dictionary.keys():
        #     try:
        #         # Update inverted index and posting
        #         if term not in self.inverted_idx.keys():
        #             self.inverted_idx[term] = 1
        #             self.postingDict[term] = []
        #         else:
        #             self.inverted_idx[term] += 1
        #         self.postingDict[term].append((document.tweet_id, document_dictionary[term])) #tf
        #
        #     except:
        #         print('problem with the following key {}'.format(term[0]))
