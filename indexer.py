import math

from PostingbyTerm import PostingbyTerm
from memoryposting import MemoryPosting


class Indexer:
    def __init__(self, config):
        self.inverted_idx = {}  ## key=term    value=( numOfDoc , TotalnumberInCorpus ,pointerToPosting )
        self.postingDict = {} ##key=term   value=postingd
        #self.config = config

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
        postings = {}   ##key=term  value=(docID,tweetID,tf,tfi)
        max_term = 0  # number of maximum  word interfaces per doc
        #m = MemoryPosting()

        # document=updateDocByEntity
        for word in document:
            if word in postings.keys():
                postings[word].tfi += 1
            else:  # first doc of this word
                word.numOfDoc += 1
                postings[word] = PostingbyTerm(document_index,tweetID)
            max_term = max(max_term, postings[word].tfi)

        for word in postings.keys():
            postings[word].tfi = postings[word].tfi / max_term  ## tfij=fij/max{fj}
            if word in self.postingDict.keys():
                self.postingDict[word].append(postings[word])
            else:
                self.postingDict[word] = [postings[word]]


    def CreatInvertedIndex(self,word_dict,idx):
        self.inverted_idx = {} ##key:str name value: start,size,idfi=log(N/dfi)
        N = idx
        for word in word_dict.keys():
            if word_dict[word].numOfDoc == 0:
                continue
            self.inverted_idx[word] = [-1,-1,math.log2(N/word_dict[word].numOfDoc)]
        return  self.inverted_idx












        # #document=updateDocByEntity
        # for word in document:
        #     if word in postings.keys():
        #         postings[word].tfi += 1
        #     else: #first doc of this word
        #         word.numOdDoc += 1
        #         postings[word] = PostingbyTerm(document_index, tweetID)
        #     max_term = max(max_term, postings[word].tfi)
        #
        # for word in postings.keys():
        #     postings[word].tfi = postings[word].tfi/max_term    ## tfij=fij/max{fj}
        #     if word in self.postingDict.keys():
        #         self.postingDict[word].append(postings[word])
        #     else:
        #         self.postingDict[word] = [postings[word]]
        #
        #     file = m.Save(self.postingDict)
        #     self.inverted_idx[word].append(file)

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
