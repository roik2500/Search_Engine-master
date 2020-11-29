import os
import struct


class BinaryMemoryPosting:
    __slots__ = ['postingFile', 'count', 'dir']

    def __init__(self, posting_file):
        self.postingFile = posting_file
        self.count = 0
        self.dir = 'tempPost'  # name of file of posting file
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

    # Creating a new txt file for posting file and writing the Data
    def Save(self, posting_dict):
        file = open(f'{self.dir}/{self.count}.bin', 'wb')

        for post in posting_dict.keys():
            data = self.createPostData(posting_dict[post].postings)
            file.write(data)
            posting_dict[post].postings.clear()
        file.close()
        self.count += 1

    @staticmethod
    def createPostData(data):
        """
           This function creating the content of each posting file(before merge)
           format: term~#(idx,docId,tfi)
          :param data
          :return: str list of all the data by the format above
         """
        output = struct.pack('I', len(data) * 24)
        for d in data:
            output += struct.pack('IQd', d.docId, int(d.tweetId), d.tfi)
        return output

    def Merge(self, inverted_index):
        """
        This function merging all the posting file to one file
        :param inverted_index
        :return: -
         """
        # open all files
        files = [open(f'{self.dir}/{i}.bin', 'rb') for i in range(self.count)]
        merged_file = open(self.postingFile, 'wb')  # the new files of all posting files
        curr_offset = 0
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
            if inverted_index[term]:
                merged_file.write(struct.pack('I', len(line)))
                merged_file.write(line)
                inverted_index[term.lower()][0] = curr_offset
                curr_offset += len(line) + 4
        for file in files:
            file.close()
            os.remove(file.name)
        merged_file.close()
        for term in list(inverted_index.keys()):
            if not inverted_index[term]:
                inverted_index.pop(term)
