import math

from PostingbyTerm import PostingbyTerm
from memoryposting import MemoryPosting


class Indexer:
    def __init__(self, config):
        self.inverted_idx = {}  ## key=term    value=( numOfDoc , TotalnumberInCorpus ,pointerToPosting )
        self.postingDict = {}  ##key=term     value=postingd
        self.global_Table = {}  ##key=term_1     value={term_2:score}
        self.entity = {}

    def addEntityToLastPosting(self):
        for entity in self.entity.keys():
            if len(entity.listOfDoc)>=2:
                self.postingDict[entity]=self.entity[entity]
        return self.postingDict


    def add_new_doc(self, document, document_index, tweetID):
        """
        This function perform indexing process for a document list.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document:list of term (object term),int document_index (docId), int tweetid
        :return: -void
        """

        # Go over each term in the doc
        # this structur include a postingbyTerm object
        postings = {}  ##key=term  value=(docID,tweetID,tf,tfi)
        max_term = 0  # number of maximum  word interfaces per doc
        self.addTOGlobalMethod(document)
        # document=updateDocByEntity
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
            sigma += postings[word].tfi**2
            if word.isentity():pd=self.entity
            else:pd=self.postingDict
            if word in pd.keys():
                pd[word].append(postings[word])
            else:
                pd[word] = [postings[word]]

        if sigma !=0: sigma = 1/math.sqrt(sigma)
        for word in postings.keys():
             postings[word].tfi *= sigma


    def addTOGlobalMethod(self, Document):
        """
        This function are updating the global table
        The function taking two words any time from list and calculate the colorization between them
        :param Document: list of term (object term)
        :return: void
        """
        for word_1 in Document:
            if word_1 not in self.global_Table.keys(): self.global_Table[word_1] = {}
            for word_2 in Document:
                #if word_1 == word_2: continue
                if word_2 not in self.global_Table[word_1].keys():
                    self.global_Table[word_1][word_2] = 0
                self.global_Table[word_1][word_2] += 1

    def CreatInvertedIndex(self, word_dict, idx):
        self.inverted_idx = {}  ##key:str name value: start,size,idfi=log(N/dfi)
        N = idx + 1
        for word in word_dict.keys():
            if word_dict[word].isentity() and len(word_dict[word].listOfDoc) < 2: continue
            if word_dict[word].numOfDoc == 0:
                continue
            self.inverted_idx[word] = [-1, -1, math.log2(N / word_dict[word].numOfDoc),
                                       self.BestFourWord(word_dict[word])]
        return self.inverted_idx

    def BestFourWord(self, word):
        """"
        This function finding the best 4 word are simultaneity with word by the colorization
        by the global method
        :param str word
        :return list of (name of term,score of term)
        """
        best = []
        for opt in self.global_Table[word].items():
            sij=opt[1]/(self.global_Table[word][word]+self.global_Table[opt[0]][opt[0]]-opt[1])
            if len(best) < 4:
                best.append((opt[0],sij))
                best.sort(key=lambda s: s[1])
            elif opt[1] > best[0][1]:
                best[0] = (opt[0],sij)
                best.sort(key=lambda s: s[1])
        return [(b[0].text.lower(), b[1]) for b in best]

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
