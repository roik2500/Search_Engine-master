import os


class MemoryPosting:
    def __init__(self,postingFile):
        self.postingFile = postingFile
        self.count = 0
        self.dir = 'tempPost' #name of file of postingfile
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)


    ##Creating a new txt file for posting file and writing the Data
    def Save(self, postingdict ): #TODO: improve protocol
        file = open(f'{self.dir}/{self.count}.txt','w')

        for post in postingdict.keys():
             data = self.createPostData(post,postingdict[post])
             file.write(data)
             postingdict[post].clear()
        file.close()
        self.count += 1


    def createPostData(self,term,data):
        """
           This function creating the content of each posting file(befor merge)
           format: term~#(idx,docId,tfi)
          :param dict invertedindex
          :return: str list of all the data by the format above
         """
        output = term.text+'~#'
        for d in data:
            output +='('+str(d.docId)+','+str(d.tweetId)+ ','+str(d.tfi)+')'
        output += '\n'
        return output



    def Merge(self,inverted_index):
        """
        This function mergin all the posting file to one file
        :param dict invertedindex
        :return: -
         """
        ## open all files
        files = [open(f'{self.dir}/{i}.txt','r') for i in range(self.count)]
        merged_file = open(self.postingFile,'w') #the new files of all posting files
        curroffset = 0
        all_done = False
        while not all_done:
            term = ''
            new_line = ''
            all_done = True
            for file in files:
                line = file.readline()
                if line:
                    all_done = False
                    line = line.strip('\n').split('~#') ##remove '\n'
                    if term == '':
                        term = line[0]
                        new_line += term+'~#'
                    new_line += line[1]
            if not all_done:
                new_line += '\n'
                inverted_index[term.lower()][0] = curroffset
                inverted_index[term.lower()][1] = merged_file.write(new_line)
                curroffset += inverted_index[term.lower()][1] + 1
        for file in files:
            file.close()
            os.remove(file.name)
        merged_file.close()


