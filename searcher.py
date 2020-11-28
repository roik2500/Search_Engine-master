import struct
from parser_module import Parse
from ranker import Ranker


class Searcher:
    __slots__ = ['parser','ranker','inverted_index','postingfile']
    def __init__(self, inverted_index, postingfile=None):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.parser = Parse()
        self.ranker = Ranker()
        self.inverted_index = inverted_index
        self.postingfile = postingfile

    def CalculateW(self, query):
        output = {}
        # add=[]
        # source=query.copy()
        # for q in query:
        #     if q not in self.inverted_index.keys():continue
        #     add+=[x[0] for x in self.inverted_index[q][2]]

        #     for x in self.inverted_index[q][3]:
        #         if x[0] in output.keys():
        #             output[x[0]] += x[1]
        #         else:
        #             output[x[0]] = x[1]
        #         maxterm = max(maxterm, output[x[0]])
        #
        # for word in output.keys():
        #     if word not in self.inverted_index: continue  ##if word not in our compus-->worong typing of input
        #     output[word] = 0.5 *  (output[word] / maxterm) * self.inverted_index[word][2]  # wiq=tf*idf
        # query+=add

        maxterm = 0
        for word in query:
            if word in output.keys():
                output[word] += 1
            else:
                output[word] = 1
            maxterm = max(maxterm, output[word])

        for word in output.keys():
            if word not in self.inverted_index: continue  ##if word not in our compus-->worong typing of input
            output[word] = (output[word] / maxterm) * self.inverted_index[word][1] # wiq=tf*idf
        return output

    def relevant_docs_from_posting(self, query):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query: list of term object (query)
        :return: dictionary of relevant documents.
        """
        relevant_docs = {}
        # postingLists = [self.FindPostingByTerm(term) for term in query]  #list of postingfile -->[idx,tweetid,tfi]
        for term in query:
            try:
                # post = self.FindPostingByTerm(term)
                post = self.FindPostingByTerm_Binary(term)
                for p in post:
                    tweetId = p[1]
                    if tweetId not in relevant_docs.keys():
                        relevant_docs[tweetId] = {}
                    relevant_docs[tweetId][term] = p[2] * self.inverted_index[term][1]  # wiq
            except:
                print('term {} not found in posting'.format(term))
        return relevant_docs


    def FindPostingByTerm(self, term):
        if term not in self.inverted_index.keys():
            print("the term {} not in inverted index ".format(term))
            return None
        data = None
        with open(self.postingfile, 'r') as file:
            start = self.inverted_index[term][0]
            size = self.inverted_index[term][1]
            file.seek(start)
            data = file.read(size - 1)
            data = data.split('~#')[1]
            data = data[1:-1].split(')(')
            data = [self.read_data(d) for d in data]
        return data

    def read_data(self, data):
        d = data.split(',')
        return (int(d[0]), d[1], float(d[2]))


    def FindPostingByTerm_Binary(self, term):
        if term not in self.inverted_index.keys():
            print("the term {} not in inverted index ".format(term))
            return None
        data = None
        with open(self.postingfile, 'rb') as file:
            start = self.inverted_index[term][0]
            file.seek(start)
            size = struct.unpack('I', file.read(4))[0]
            data = file.read(size)
            data = [self.read_bin_data(data[i:i+24]) for i in range(0, len(data), 24)]
        return data

    def read_bin_data(self, data):
        return (struct.unpack('Q',data[:8])[0], struct.unpack('Q',data[8:16])[0], struct.unpack('d',data[16:])[0])
