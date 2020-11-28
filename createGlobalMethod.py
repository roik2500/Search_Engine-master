import utils
from configuration import ConfigClass
from indexer import Indexer
from parser_module import Parse
from reader import ReadFile




def run_engine():
    """
    :return:
    """
    global_Table={}
    config = ConfigClass()
    r = ReadFile(corpus_path=config.get__corpusPath())
    p = Parse()
    p.UseStemmer = config.DoStemmer
    # m = MemoryPosting(config.PostingFile)


    # Iterate over every document in the file
    idx = 0
    for documents_list in r:
        step = 1/len(documents_list)
        #play(documents_list,indexer,p,config,idx,parse_limit,m)
        for document in documents_list:
            # print(document)
            # parse the document
            ## parsed_document = p.parse_doc(document)
            parsed_list = p.parse_doc(document, idx)
            # break
            # number_of_documents += 1
            print(idx)

            # index the document data
            addTOGlobalMethod(parsed_list,global_Table)
            # print(idx)
            idx += 1
    utils.save_obj(global_Table, 'global_table')

def addTOGlobalMethod(Document,global_Table):
    """
    This function are updating the global table
    The function taking two words any time from list and calculate the colorization between them
    :param Document: list of term (object term)
    :return: void
    """
    for word_1 in Document:
        if word_1 not in global_Table.keys(): global_Table[word_1] = {}
        for word_2 in Document:
            #if word_1 == word_2: continue
            if word_2 not in global_Table[word_1].keys():
                global_Table[word_1][word_2] = 0
            global_Table[word_1][word_2] += 1

run_engine()
