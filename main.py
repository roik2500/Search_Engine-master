import search_engine

if __name__ == '__main__':
    corpus_path= r'..\Dataa'
    output_path=''
    stemming=True
    #queries='queries.txt'
    queries=['Houston']
    num_docs_to_retrieve=3

    search_engine.main(corpus_path, output_path, stemming, queries, num_docs_to_retrieve)
    # search_engine.main()

