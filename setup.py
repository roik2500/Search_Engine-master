import nltk
import search_engine

nltk.download('stopwords')
nltk.download('punkt')

corpus_path= r'../Data'
output_path=''
stemming = True
# queries = 'queries.txt'
queries = ['donald trump']

num_docs_to_retrieve = 5

search_engine.main(corpus_path,output_path,stemming,queries,num_docs_to_retrieve)
# search_engine.main()