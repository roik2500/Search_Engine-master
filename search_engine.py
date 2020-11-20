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
    m = MemoryPosting()
    indexer = Indexer(config)
    maxpostingsize=100

    # Iterate over every document in the file
    idx = 0
    for documents_list in r:
        for document in documents_list:
            if idx == 1000:return
            # parse the document
            ## parsed_document = p.parse_doc(document)
            parsed_list = p.parse_doc(document)

            ## if len(p.returnEntity()) >= 1:
            ##  updateDocByEntity(parsed_document, p.returnEntity())

            # break
            #number_of_documents += 1
            print(idx)

            # index the document data
            indexer.add_new_doc(parsed_list,idx,document[0])
            idx += 1
            if idx % maxpostingsize == 0:
                m.Save(indexer.postingDict)

    inv_index = CreatInvertedIndex(p.word_dict)
    print('Finished parsing and indexing. Starting to export files')
    m.Merge(inv_index)
    utils.save_obj(inv_index,'inverted_idx')

def CreatInvertedIndex(word_dict):
    return #TODO: implement



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
    p = Parse()
    query_as_list = p.parse_sentence(query)
    searcher = Searcher(inverted_index)
    relevant_docs = searcher.relevant_docs_from_posting(query_as_list)
    ranked_docs = searcher.ranker.rank_relevant_doc(relevant_docs)
    return searcher.ranker.retrieve_top_k(ranked_docs, k)


# def main(corpus_path,output_path,stemming,queries,num_docs_to_retrieve):
def main():
    start_time = time.time()
    run_engine()
    print("--- %s seconds ---" % (time.time() - start_time))

    query = input("Please enter a query: ")
    k = int(input("Please enter number of docs to retrieve: "))
    inverted_index = load_index()
    for doc_tuple in search_and_rank_query(query, inverted_index, k):
        print('tweet id: {}, score (unique common words with query): {}'.format(doc_tuple[0], doc_tuple[1]))
