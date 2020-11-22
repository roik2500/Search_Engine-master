class ConfigClass:
    def __init__(self):
        self.corpusPath = r'..\Dataa'
        self.savedFileMainFolder = ''
        self.saveFilesWithStem = self.savedFileMainFolder + "/WithStem"
        self.saveFilesWithoutStem = self.savedFileMainFolder + "/WithoutStem"
        self.toStem = False
        self.PostingFile = 'posting_dictionary.txt'
        self.invertedindex='inverted_file'

        # print('Project was created successfully..')

    def get__corpusPath(self):
        return self.corpusPath
