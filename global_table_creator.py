from parser_module import Parse
from reader import ReadFile
import sys
import pymongo
import utils


def create_table(stemming, corpus):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["global"]
    mycol.drop()
    r = ReadFile(corpus)
    p = Parse(stemming)
    for documents_list in r:
        step = 1 / len(documents_list)
        for document in documents_list:
            parsed_list = [t.text.lower() for t in p.parse_doc(document) if '$' not in t.text]

            for word_1 in parsed_list:
                query = {'term': word_1}
                row = mycol.find_one(query)
                if not row:
                    mycol.insert_one({**query, 'terms': {}})
                    row = mycol.find_one(query)
                for word_2 in parsed_list:
                    if word_2 not in row['terms'].keys():
                        row['terms'][word_2] = 0
                    row['terms'][word_2] += 1
                try:
                    mycol.update_one(query, {"$set": {'terms': row['terms']}})
                except:
                    print(row['terms'])

            r.progressbar.update(step)
            counter += 1
    global_table = {}
    for word_1 in mycol.find():
        top = []
        for word_2 in word_1['terms'].keys():
            s = word_1['terms'][word_2] / (
                    word_1['terms'][word_1['term']] + mycol.find_one({'term': word_2})['terms'][word_1['term']] -
                    word_1['terms'][word_2])
            if len(top) < 10:
                top.append((word_2, s))
                top.sort(key=lambda score: score[1])
            elif s > top[0][1]:
                top[0] = (word_2, s)
                top.sort(key=lambda score: score[1])
        global_table[word_1['term']] = top
    utils.save_obj(global_table, f'global_table_{stemming}')


if __name__ == '__main__':
    print('Creating Global With Stemming')
    create_table(True, sys.argv[1])
    print('Done')
    print('Creating Global Without Stemming')
    create_table(False, sys.argv[1])
    print('Done')
