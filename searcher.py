from parser_module import Parse
from ranker import Ranker
import utils


class Searcher:

    def __init__(self, inverted_index,postingfile=None):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.parser = Parse()
        self.ranker = Ranker()
        self.inverted_index = inverted_index
        self.postingfile = postingfile

    def relevant_docs_from_posting(self, query):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query: query
        :return: dictionary of relevant documents.
        """
        for term in query:
            try:  # an example of checks that you have to do
                posting_doc = posting[term]
                for doc_tuple in posting_doc:
                    doc = doc_tuple[0]
                    if doc not in relevant_docs.keys():
                        relevant_docs[doc] = 1
                    else:
                        relevant_docs[doc] += 1
            except:
                print('term {} not found in posting'.format(term))
        return relevant_docs

    def FindPostingByTerm(self,term):
        if term not in self.inverted_index.keys():
            print("the term not in inverted index "+term)
            return None
        data = None
        with open(self.postingfile,'r') as file:
            start = self.inverted_index[term][0]
            size = self.inverted_index[term][1]
            file.seek(start)
            data = file.read(size-1)
            data = data.split('~#')[1]
            data = data[1:-1].split(')(')
            data = [self.read_data(d) for d in data]
        return data

    def read_data(self,data):
        d = data.split(',')
        return (int(d[0]),d[1],float(d[2]))




