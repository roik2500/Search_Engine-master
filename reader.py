import os
import pandas as pd
from tqdm import tqdm


class ReadFile:
    __slots__ = ['corpus_path', 'progressbar', 'n', 'file_list']

    def __init__(self, corpus_path):
        self.corpus_path = corpus_path
        self.progressbar = None
        self.file_list = []
        self.n = 0

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
        self.file_list = []
        for root, dirs, files in os.walk(self.corpus_path):
            for name in files:
                if name.endswith(".parquet"):
                    self.file_list.append(os.path.join(root, name))
        self.file_list.sort()
        self.progressbar = tqdm(total=len(self.file_list))
        self.n = 0
        return self

    def __next__(self):
        if self.n >= len(self.file_list):
            raise StopIteration
        else:
            self.n += 1
            return self.read_file(self.file_list[self.n - 1])
