import json
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
    m = MemoryPosting(config.PostingFile)
    indexer = Indexer(config)
    maxpostingsize = 1000

    # Iterate over every document in the file
    idx = 0
    for documents_list in r:
        for document in documents_list:
            #print(document)
            # parse the document
            ## parsed_document = p.parse_doc(document)
            parsed_list = p.parse_doc(document,idx)
            #break
            #number_of_documents += 1
            print(idx)

            # index the document data
            indexer.add_new_doc(parsed_list,idx,document[0])
            idx += 1
            if idx % maxpostingsize == 0:
                m.Save(indexer.postingDict)
            if idx == 10000: break
        break

    inv_index = indexer.CreatInvertedIndex(p.word_dict,idx)
    print('Finished parsing and indexing. Starting to export files')
    m.Merge(inv_index)
    #utils.save_obj(inv_index,'inverted_idx')


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
    config = ConfigClass()
    inverted_index = utils.load_obj("inverted_idx")
    return inverted_index


def search_and_rank_query(query,inverted_index, k):
    config = ConfigClass()
    p = Parse()
    roi=p.parse_sentence(query)
    query_as_list = [term.text.lower() for term in roi]
    #query_as_list = p.parse_sentence(query)
    searcher = Searcher(inverted_index,config.PostingFile)
    WoftermInQuery=searcher.CalculateW(query_as_list)
    relevant_docs = searcher.relevant_docs_from_posting(WoftermInQuery.keys())
    ranked_docs = searcher.ranker.rank_relevant_doc(relevant_docs,WoftermInQuery)
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
