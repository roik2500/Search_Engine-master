import os
import pandas as pd
import glob2

class ReadFile:
    def __init__(self, corpus_path):
        self.corpus_path = corpus_path

    def read_file(self, file_name):
        """
        This function is reading a parquet file contains several tweets
        The file location is given as a string as an input to this function.
        :param file_name: string - indicates the path to the file we wish to read.
        :return: a dataframe contains tweets.
        """
        full_path = os.path.join(self.corpus_path, file_name)
        df = pd.read_parquet(full_path, engine="pyarrow")
        return df.values.tolist()


# iter for read from document
    def __iter__(self):
        self.file_list = [file for file in os.listdir(self.corpus_path) if file.endswith(".parquet")]
        self.n = 0
        return self

    def __next__(self):
        if self.n >= len(self.file_list):
            raise StopIteration
        else:
            self.n += 1
            return self.read_file(self.file_list[self.n - 1])
