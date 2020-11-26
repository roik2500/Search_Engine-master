import search_engine

if __name__ == '__main__':
    corpus_path= r'..\Dataa'
    output_path=''
    stemming = True
    # queries = 'queries.txt'
    queries = ['donald trump']

    num_docs_to_retrieve = 5

    search_engine.main(corpus_path, output_path, stemming, queries, num_docs_to_retrieve)
    # search_engine.main()

