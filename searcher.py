import struct
from ranker import Ranker


class Searcher:
    __slots__ = ['ranker', 'inverted_index', 'posting_file']

    def __init__(self, inverted_index, posting_file=None):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.ranker = Ranker()
        self.inverted_index = inverted_index
        self.posting_file = posting_file

    def CalculateW(self, query):
        output = {}

        max_term = 0
        for word in query:
            if word in output.keys():
                output[word] += 1
            else:
                output[word] = 1
            max_term = max(max_term, output[word])

        for word in output.keys():
            if word not in self.inverted_index:
                continue  # if word not in our corpus--> wrong typing of input
            output[word] = (output[word] / max_term) * self.inverted_index[word][1]  # wiq=tf*idf
        return output

    def relevant_docs_from_posting(self, query):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query: list of term object (query)
        :return: dictionary of relevant documents.
        """
        relevant_docs = {}
        # postingLists = [self.FindPostingByTerm(term) for term in query]  #list of posting file -->[idx,tweet id,tfi]
        for term in query:
            try:
                # post = self.FindPostingByTerm(term)
                post = self.FindPostingByTerm_Binary(term)
                for p in post:
                    tweet_id = p[1]
                    if tweet_id not in relevant_docs.keys():
                        relevant_docs[tweet_id] = {}
                    relevant_docs[tweet_id][term] = p[2] * self.inverted_index[term][1]  # wiq
            except:
                print('term {} not found in posting'.format(term))
        return relevant_docs

    def FindPostingByTerm_Binary(self, term):
        if term not in self.inverted_index.keys():
            print("the term {} not in inverted index ".format(term))
            return None

        with open(self.posting_file, 'rb') as file:
            start = self.inverted_index[term][0]
            file.seek(start)
            size = struct.unpack('I', file.read(4))[0]
            data = file.read(size)
            data = [self.read_bin_data(data[i:i + 24]) for i in range(0, len(data), 24)]
        return data

    @staticmethod
    def read_bin_data(data):
        return struct.unpack('Q', data[:8])[0], struct.unpack('Q', data[8:16])[0], struct.unpack('d', data[16:])[0]
