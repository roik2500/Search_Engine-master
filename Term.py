class Term:
    def __init__(self, text):
        self.text = text
        self.numOfInterfaces = 1
        self.numOfDoc = 0  #dfi

        self.listOfDoc = set() #only for entity

    def __repr__(self):
        return self.text

    def isentity(self):
        if len(self.listOfDoc) > 0:return True
        else:return False



