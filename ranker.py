import math


class Ranker:
    def __init__(self):
        pass

    @staticmethod
    def rank_relevant_doc(relevant_doc, query_grades=None):
        """
        This function provides rank for each relevant document and sorts them by their scores.
        The current score considers solely the number of terms shared by the tweet (full_text) and query.
        :param query_grades: the W grade for every term in the query
        :param relevant_doc: dictionary of documents that contains at least one term from the query.
        :return: sorted list of documents by score
        """
        sum_Wq_sqr = sum([a**2 for a in query_grades.values()])
        output = []
        for doc in relevant_doc.keys():
            sum_Wi_sqr = 0
            score = 0
            for term in relevant_doc[doc].keys():
                sum_Wi_sqr += relevant_doc[doc][term]**2
                score += query_grades[term]*relevant_doc[doc][term]# sim()
            s = score/math.sqrt(sum_Wi_sqr*sum_Wq_sqr)
            output.append((doc, s))
        return sorted(output, key=lambda item: item[1], reverse=True)

    @staticmethod
    def retrieve_top_k(sorted_relevant_doc, k=1):
        """
        return a list of top K tweets based on their ranking from highest to lowest
        :param sorted_relevant_doc: list of all candidates docs.
        :param k: Number of top document to return
        :return: list of relevant document
        """
        return sorted_relevant_doc[:k]
