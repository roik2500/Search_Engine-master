import csv
import time
from memory_posting_binary import BinaryMemoryPosting
from reader import ReadFile
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
import utils
import os

PostingFile = r'posting_dictionary.bin'
InvertedIndexFile = r'inverted_idx'
file_output = 'results.csv'


def run_engine(corpus_path, stemming, outpath):
    """
    :return:
    """
    r = ReadFile(corpus_path)
    p = Parse(stemming)
    m = BinaryMemoryPosting(PostingFile)
    indexer = Indexer()
    max_posting_size = 100000

    if os.path.exists(PostingFile):
        os.remove(PostingFile)
    if os.path.exists(InvertedIndexFile + '.pkl'):
        os.remove(InvertedIndexFile + '.pkl')

    # Iterate over every document in the file
    idx = 0
    #parquet_number = 1
    for documents_list in r:
        step = 1 / len(documents_list)
        for document in documents_list:
            parsed_list = p.parse_doc(document)

            # index the document data
            indexer.add_new_doc(parsed_list, idx, document[0])
            idx += 1

            if idx % max_posting_size == 0:
                m.Save(p.word_dict)
            r.progressbar.update(step)


        #this code for building the global method table
        # if parquet_number == 1:
        #     first = True
        # else:first = False

        # this code are creating the global table per parquet
        #indexer.Creat_and_load_global_table(first)
        #parquet_number += 1


    r.progressbar.close()
    m.Save(p.word_dict)

    if stemming==True:
        global_table = utils.load_obj('global_table_withStemming')
    else:
        global_table = utils.load_obj('global_table_noStwmming')

    inv_index = indexer.CreatInvertedIndex(p.word_dict, idx,global_table)
    m.Merge(inv_index)
    utils.save_obj(inv_index, InvertedIndexFile)


# This function for update the doc,addingv the entity that appears at least in tow doc in all the corpus
def updateDocByEntity(doc, list_of_entity):
    for term in list_of_entity:  # tf
        if term not in doc.term_dict.keys():
            doc.term_dict[term] = 1
        else:
            doc.term_dict[term] += 1
    return doc


def load_index():
    print('Load inverted index')
    inverted_index = utils.load_obj(InvertedIndexFile)
    return inverted_index


def search_and_rank_query(query, inverted_index, k, stemming):
    p = Parse(stemming)

    query_as_list = [term.text.lower() for term in p.parse_sentence(query)]

    searcher = Searcher(inverted_index, PostingFile)

    w_of_term_in_query = searcher.CalculateW(query_as_list)

    relevant_docs = searcher.relevant_docs_from_posting(list(w_of_term_in_query.keys()))

    ranked_docs = searcher.ranker.rank_relevant_doc(relevant_docs, w_of_term_in_query)
    output = searcher.ranker.retrieve_top_k(ranked_docs, k)
    return output


def main(corpus_path, output_path, stemming, queries, num_docs_to_retrieve):
    run_engine(corpus_path, stemming, output_path)
    inverted_index = load_index()

    if not isinstance(queries, list):
        queries = ReadQueryFromFile(queries)
    file = open(file_output, 'w', newline='')
    csv.writer(file).writerow(["tweetID", "score"])
    for q in queries:
        print(q)  # TODO: remove
        for doc_tuple in search_and_rank_query(q, inverted_index, num_docs_to_retrieve, stemming):
            csv.writer(file).writerow(["{:f}".format(doc_tuple[0]),"{:f}".format(doc_tuple[1])])
            print('tweet id: {}, score : {}'.format(doc_tuple[0], doc_tuple[1]))#TODO: remove
    file.close()


def ReadQueryFromFile(queries_file):
    """
    This function received a file of queries and return a list of queries that any index in list is query
    :param queries_file:
    :return:list of queries
    """
    file = open(queries_file, encoding="utf8")
    queries = []
    lines = file.readlines()
    for line in lines:
        if line == '\n':
            continue
        queries.append(line[(line.find('.') + 1):].strip('\n'))
    file.close()
    return queries
