class PostingByTerm:
    __slots__ = ['docId', 'tweetId', 'tfi']

    def __init__(self, doc_id, tweet_id):
        self.docId = doc_id
        self.tweetId = tweet_id
        self.tfi = 1  # number of interfaces in doc_id
