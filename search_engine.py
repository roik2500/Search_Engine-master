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

    parse_limit = -1

    limit_input = input('Number of tweets to index(leave empty for entire corpus):')
    while True:
        if limit_input == '':
            break
        try:
            parse_limit = int(limit_input)
            break
        except:
            print('Wrong Input')
            limit_input = input('Number of tweets to index(leave empty for entire corpus):')

    # Iterate over every document in the file
    idx = 0
    for documents_list in r:
        step = 1 / len(documents_list)
        for document in documents_list:
            parsed_list = p.parse_doc(document)

            # index the document data
            indexer.add_new_doc(parsed_list, idx, document[0])
            # print(idx)
            idx += 1

            if idx % max_posting_size == 0:
                m.Save(p.word_dict)
            r.progressbar.update(step)

            if idx == parse_limit:
                break
        if idx == parse_limit:
            break
    r.progressbar.close()
    m.Save(p.word_dict)
    # indexer.Creat_and_load_global_table()

    print('Creating Inverted Index')
    inv_index = indexer.CreatInvertedIndex(p.word_dict, idx)
    print('Finished parsing and indexing. Starting to export files')
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

    # start_time = time.time()
    query_as_list = [term.text.lower() for term in p.parse_sentence(query)]
    # print("query parse --- %s seconds ---" % (time.time() - start_time))

    # query_as_list = p.parse_sentence(query)
    searcher = Searcher(inverted_index, PostingFile)

    # start_time = time.time()
    w_of_term_in_query = searcher.CalculateW(query_as_list)
    # print("Calculate query W --- %s seconds ---" % (time.time() - start_time))

    # start_time = time.time()
    relevant_docs = searcher.relevant_docs_from_posting(list(w_of_term_in_query.keys()))
    # print("relevant docs --- %s seconds ---" % (time.time() - start_time))

    # start_time = time.time()
    ranked_docs = searcher.ranker.rank_relevant_doc(relevant_docs, w_of_term_in_query)
    output = searcher.ranker.retrieve_top_k(ranked_docs, k)
    # print("rank docs --- %s seconds ---" % (time.time() - start_time))
    return output


def main(corpus_path, output_path, stemming, queries, num_docs_to_retrieve):
    print("<------------- COVID Tweet Searcher ------------->")
    rebuild_index = input("Rebuild Index?[Y,n]")
    while rebuild_index.lower() not in ['', 'y', 'n']:
        print('Wrong Input')
        rebuild_index = input("Rebuild Index?[Y,n]")

    start_time = time.time()
    if rebuild_index == '' or rebuild_index.lower() == 'y':
        run_engine(corpus_path, stemming)

    print("--- %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    inverted_index = load_index()
    print("inverted index load --- %s seconds ---" % (time.time() - start_time))

    output_file = None
    if output_path:
        output_file = open(output_path, 'w')

    if queries == '':
        while True:
            q = input("query: ")
            for doc_tuple in search_and_rank_query(q, inverted_index, num_docs_to_retrieve, stemming):
                if output_file:
                    output_file.write('tweet id: {}, score : {}\n'.format(doc_tuple[0], doc_tuple[1]))
                else:
                    print('tweet id: {}, score : {}'.format(doc_tuple[0], doc_tuple[1]))
    else:
        if not isinstance(queries, list):
            queries = ReadQueryFromFile(queries)
        for q in queries:
            print(q)  # TODO: remove
            for doc_tuple in search_and_rank_query(q, inverted_index, num_docs_to_retrieve, stemming):
                if output_file:
                    output_file.write('tweet id: {}, score : {}\n'.format(doc_tuple[0], doc_tuple[1]))
                else:
                    print('tweet id: {}, score : {}'.format(doc_tuple[0], doc_tuple[1]))


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
