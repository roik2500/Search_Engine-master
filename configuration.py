class ConfigClass:
    def __init__(self):
        self.corpusPath = r'../Dataa'
        self.savedFileMainFolder = ''
        self.saveFilesWithStem = self.savedFileMainFolder + "/WithStem"
        self.saveFilesWithoutStem = self.savedFileMainFolder + "/WithoutStem"
        self.DoStemmer = False
        # self.PostingFile = 'posting_dictionary.txt'
        self.PostingFile = 'posting_dictionary.bin'
        self.output_path=''


        # print('Project was created successfully..')

    def get__corpusPath(self):
        return self.corpusPath

    def set__corpusPath(self,corpusPath):
        self.corpusPath=corpusPath

    def set__output_path(self,output_path):
        self.output_path=output_path
