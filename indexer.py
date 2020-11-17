class Indexer:

    def __init__(self, config):
        self.inverted_idx = {} ## key=term  value=(numOfDoc,TotalnumberInCorpus,pointerToPosting)
        self.postingDict = {}

        self.config = config
        self.numberOfDocuments = 0   ## N

    def add_new_doc(self, document):
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """
        self.numberOfDocuments += 1
        document_dictionary = document.term_doc_dictionary
        # Go over each term in the doc
        for term in document_dictionary.keys():
            try:
                # Update inverted index and posting
                if term not in self.inverted_idx.keys():
                    self.inverted_idx[term] = 1
                    self.postingDict[term] = []
                else:
                    self.inverted_idx[term] += 1
                self.postingDict[term].append((document.tweet_id, document_dictionary[term])) #tf

            except:
                print('problem with the following key {}'.format(term[0]))
