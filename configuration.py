class ConfigClass:
    def __init__(self):
        self.corpusPath = r'C:\Users\roik2\PycharmProjects\pythonProject\Dataa'
        self.savedFileMainFolder = ''
        self.saveFilesWithStem = self.savedFileMainFolder + "/WithStem"
        self.saveFilesWithoutStem = self.savedFileMainFolder + "/WithoutStem"
        self.toStem = False

        print('Project was created successfully..')

    def get__corpusPath(self):
        return self.corpusPath
