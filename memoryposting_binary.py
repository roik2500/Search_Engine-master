import os
import struct

class BinaryMemoryPosting:
    def __init__(self,postingFile):
        self.postingFile = postingFile
        self.count = 0
        self.dir = 'tempPost' #name of file of postingfile
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)


    ##Creating a new txt file for posting file and writing the Data
    def Save(self, postingdict ): #TODO: improve protocol
        file = open(f'{self.dir}/{self.count}.txt', 'wb')

        for post in postingdict.keys():
             data = self.createPostData(postingdict[post])
             file.write(data)
             postingdict[post].clear()
        file.close()
        self.count += 1


    def createPostData(self, data):
        """
           This function creating the content of each posting file(befor merge)
           format: term~#(idx,docId,tfi)
          :param dict invertedindex
          :return: str list of all the data by the format above
         """
        output = struct.pack('I', len(data)*24)
        for d in data:
            output += struct.pack('IQd', d.docId, int(d.tweetId), d.tfi)
        return output



    def Merge(self,inverted_index):
        """
        This function mergin all the posting file to one file
        :param dict invertedindex
        :return: -
         """
        ## open all files
        files = [open(f'{self.dir}/{i}.txt','rb') for i in range(self.count)]
        merged_file = open(self.postingFile,'wb') #the new files of all posting files
        curroffset = 0
        for term in inverted_index.keys():
            line = struct.pack('')
            for file in list(files):
                line_size = file.read(4)
                if not line_size:
                    file.close()
                    files.remove(file)
                    os.remove(file.name)
                else:
                    line += file.read(struct.unpack('I', line_size)[0])
            merged_file.write(struct.pack('I', len(line)))
            merged_file.write(line)
            inverted_index[term.lower()][0] = curroffset
            inverted_index[term.lower()][1] = len(line) + 4
            curroffset += inverted_index[term.lower()][1]
        for file in files:
            file.close()
            os.remove(file.name)
        merged_file.close()


