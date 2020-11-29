import nltk
import search_engine
import configuration

nltk.download('stopwords')
nltk.download('punkt')

search_engine.main(**configuration.config)
