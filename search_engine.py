import time
from memoryposting import MemoryPosting
from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
import utils


def run_engine():
    """
    :return:
    """
    number_of_documents = 0
    config = ConfigClass()
    r = ReadFile(corpus_path=config.get__corpusPath())
    p = Parse()
    p.UseStemmer = config.DoStemmer
    m = MemoryPosting(config.PostingFile)
    indexer = Indexer(config)
    maxpostingsize = 1000

    # Iterate over every document in the file
    idx = 0
    for documents_list in r:
        for document in documents_list:
            # print(document)
            # parse the document
            ## parsed_document = p.parse_doc(document)
            parsed_list = p.parse_doc(document, idx)
            # break
            # number_of_documents += 1
            # print(idx)

            # index the document data
            indexer.add_new_doc(parsed_list, idx, document[0])
            idx += 1
            if idx % maxpostingsize == 0:
                m.Save(indexer.postingDict)

            if idx == 100000:
                break
        if idx == 100000:
            break

    inv_index = indexer.CreatInvertedIndex(p.word_dict, idx)

    print('Finished parsing and indexing. Starting to export files')
    m.Merge(inv_index)
    utils.save_obj(inv_index, 'inverted_idx')


# This function for update the doc,adding the entity that appears at least in tow doc in all the corpus
def updateDocByEntity(doc, list_of_entity):
    for term in list_of_entity:  # tf
        if term not in doc.term_dict.keys():
            doc.term_dict[term] = 1
        else:
            doc.term_dict[term] += 1
    return doc


def load_index():
    print('Load inverted index')
    inverted_index = utils.load_obj("inverted_idx")
    return inverted_index


def search_and_rank_query(query, inverted_index, k):
    config = ConfigClass()
    p = Parse()

    # start_time = time.time()
    query_as_list = [term.text.lower() for term in p.parse_sentence(query)]
    # print("query parse --- %s seconds ---" % (time.time() - start_time))

    # query_as_list = p.parse_sentence(query)
    searcher = Searcher(inverted_index, config.PostingFile)

    # start_time = time.time()
    WoftermInQuery = searcher.CalculateW(query_as_list)
    # print("Calculate query W --- %s seconds ---" % (time.time() - start_time))

    # start_time = time.time()
    relevant_docs = searcher.relevant_docs_from_posting(list(WoftermInQuery.keys()))
    # print("relevent docs --- %s seconds ---" % (time.time() - start_time))

    # start_time = time.time()
    ranked_docs = searcher.ranker.rank_relevant_doc(relevant_docs, WoftermInQuery)
    output = searcher.ranker.retrieve_top_k(ranked_docs, k)
    # print("rank docs --- %s seconds ---" % (time.time() - start_time))
    return output


# def main(corpus_path,output_path,stemming,queries,num_docs_to_retrieve):
def main():
    # config.set__corpusPath(corpus_path)
    # config.set__output_path(output_path)
    # config.DoStemmer = stemming
    # readqueryfromfile(queries)
    # ReadQueryFromFile('queries.txt')
    start_time = time.time()
    # run_engine(config)
    # run_engine()

    print("--- %s seconds ---" % (time.time() - start_time))

    query = input("Please enter a query: ")
    k = int(input("Please enter number of docs to retrieve: "))
    start_time = time.time()
    inverted_index = load_index()
    print("inverted index load --- %s seconds ---" % (time.time() - start_time))

    for doc_tuple in search_and_rank_query(query, inverted_index, k):
        print('tweet id: {}, score (unique common words with query): {}'.format(doc_tuple[0], doc_tuple[1]))


def ReadQueryFromFile(queries_file):  # TODO: implement
    """
    This function recived a file of queries and return a list of queries that any index in list is query
    :param queries.txt
    :return:list of queries
    """
    file = open(queries_file, encoding="utf8")
    queries = []
    lines = file.readlines()
    for line in lines:
        queries.append(lines[2:-1])
    file.close()
    return queries
