from nltk.stem.porter import PorterStemmer

class Stemmer:
    def __init__(self):
        self.stemmer = PorterStemmer()

    def stem_term(self, token):
        """
        This function stem a token
        :param token: string of a token
        :return: stemmed token
        """
        word = str(token)
        if word.title():
            self.stemmer.stem(word).capitalize()
        elif word.isupper():
            self.stemmer.stem(word).upper()
        else:
            self.stemmer.stem(word)
        return word
