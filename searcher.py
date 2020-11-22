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

    def CalculateW(self,query):
        maxterm = 0
        output = {}
        for word in query:
            if word in output.keys():
                output[word] += 1
            else: output[word] = 1
            maxterm = max(maxterm,output[word])

        for word in output.keys():
            output[word] = (output[word]/maxterm)*self.inverted_index[word][2]

        return output



    def relevant_docs_from_posting(self, query):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query: list of term object (query)
        :return: dictionary of relevant documents.
        """
        output={}
        postingLists = [self.FindPostingByTerm(term) for term in query]  #list of postingfile -->[idx,tweetid,tfi]
        query_size = len(query)
        lists_indx = [0]*query_size #pointers to postingdlist

        ## check if we finish to read all the posting file (just one)
        while not [True for i in range(query_size) if lists_indx[i]>=len(postingLists[i])]:
            docs = {postingLists[i][lists_indx[i]][1] for i in range(query_size)}#list of docid
            if len(docs)==1: #all the terms from query in this docid
                tweetid=docs.pop()
                output[tweetid]={}
                for i in range(query_size):
                    output[tweetid][query[i]] = postingLists[i][lists_indx[i]][2]*self.inverted_index[query[i]][2] #wiq
                    lists_indx[i]+=1
            else:
                min_index=0
                for i in range(1,query_size):
                    if postingLists[i][lists_indx[i]][0]<postingLists[i][lists_indx[min_index]][0]: min_index=i
                lists_indx[i]+=1
        return output






        # for term in query:
        #       self.FindPostingByTerm(term)
        #     try:  # an example of checks that you have to do
        #         list_of_terms = query[term]
        #         for doc_tuple in posting_doc:
        #             doc = doc_tuple[0]
        #             if doc not in relevant_docs.keys():
        #                 relevant_docs[doc] = 1
        #             else:
        #                 relevant_docs[doc] += 1
        #     except:
        #         print('term {} not found in posting'.format(term))
        # return relevant_docs

    # [
    #     {tweetId1:
    #          {term:w}}
    # ]

    def FindPostingByTerm(self,term):
        if term not in self.inverted_index.keys():
            print("the term not in inverted index "+term)
            return None
        data = None
        with open(self.postingfile,'r') as file:
            inv = self.inverted_index
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




