class Term:
    def __init__(self, text):
        self.text = text
        self.numOfInterfaces = 1
        self.numOfDoc = 0  #dfi
        self.is_entity = False
        self.postings = []

    def __repr__(self):
        return self.text

    def isentity(self):
        return self.is_entity



