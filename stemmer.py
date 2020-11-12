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
        if word == word.title():
            word = self.stemmer.stem(word).capitalize()
        elif word.isupper():
            word = self.stemmer.stem(word).upper()
        else:
            word = self.stemmer.stem(word)
        return word
