class MemoryPosting:
    def __init__(self):
        self.count = 0
        self.dir = 'tempPost' #name of file of postingfile


    ##Creating a new txt file and writing the Data
    def Save(self, postingdict ): #TODO: improve protocol
        file = open(f'{self.dir}\\{self.count}.txt','w')
        for post in postingdict.keys():
            data = self.createPostData(post,postingdict[post])
            file.write(data)
            postingdict[post].clear()
        file.close()
        self.count += 1


    def createPostData(self,term,data):
        output = term.text
        for d in data:
            output +=  '   $    ' + str(d.docId) + ',' +str(d.tweetId)+ ',' +str(d.tfi)
        output += '\n'
        return output



    def Merge(self):
        # TODO: implement
        return