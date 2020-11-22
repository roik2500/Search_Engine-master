import json

import utils


class MemoryPosting:
    def __init__(self,postingFile):
        self.postingFile=postingFile
        self.count = 0
        self.dir = 'tempPost' #name of file of postingfile


    ##Creating a new txt file and writing the Data
    def Save(self, postingdict ): #TODO: improve protocol
        file = open(f'{self.dir}\\{self.count}.txt','w')
        # with open(f'{self.dir}\\{self.count}.json', "w+") as file:
        #     json.dump(postingdict,file,sort_keys=True)

        for post in postingdict.keys():
             data = self.createPostData(post,postingdict[post])
             file.write(data)
             postingdict[post].clear()
        file.close()
        self.count += 1


    def createPostData(self,term,data):
        output = term.text+'~#'
        for d in data:
            output +='('+str(d.docId)+','+str(d.tweetId)+ ','+str(d.tfi)+')'
        output += '\n'
        return output



    def Merge(self,inverted_index):
        ## open all files
        files = [open(f'{self.dir}\\{i}.txt','r') for i in range(self.count)]
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
                curroffset += inverted_index[term.lower()][1]+1
        for file in files:
            file.close()
        merged_file.close()
        utils.save_obj(inverted_index,'inverted_file')


