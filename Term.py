class Term:
    def __init__(self, text):
        self.text = text
        self.numOfInterfaces = 1
        self.numOfDoc = 0  #dfi
        self.listOfDoc = set()

    def __repr__(self):
        return self.text



