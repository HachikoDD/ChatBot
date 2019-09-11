
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import numpy
import pandas
from dbUtil.recordDBUtil import search_by_course, search_all
from collections import Counter

stop_words = set({'ourselves', 'hers', 'between', 'yourself', 'again',
'there', 'about', 'once', 'during', 'out', 'very', 'having',
'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its',
'yours', 'such', 'into', 'of', 'most', 'itself', 'other',
'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him',
'each', 'the', 'themselves', 'below', 'are', 'we',
'these', 'your', 'his', 'through', 'don', 'me', 'were',
'her', 'more', 'himself', 'this', 'down', 'should', 'our',
'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had',
'she', 'all', 'no', 'at', 'any', 'before', 'them',
'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does',
'yourselves', 'then', 'that', 'because', 'over',
'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you',
'herself', 'has', 'just', 'where', 'too', 'only', 'myself',
'those', 'i', 'after', 'few', 't', 'being',
'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it',
'how', 'further', 'was', 'here', 'than', 'yes', 'sorry', '92', '80','something','100',
'75'})

course_dict = {}

def get_word_dict(course_name):
    if course_name in course_dict:
        return course_dict[course_name]
    result_dict = {}
    if course_name == "all":
        questions, key_list = search_all()
    else:
        questions, key_list = search_by_course(course_name)
    if len(questions) == 0:
        return None
    corpus = questions
    new_stop_words = list(stop_words)
    new_stop_words.append(course_name)
    vectorizer=CountVectorizer(stop_words=new_stop_words)
    transformer=TfidfTransformer()
    X=vectorizer.fit_transform(corpus)
    tfidf=transformer.fit_transform(X)
    tFIDFDataFrame = pandas.DataFrame(tfidf.toarray())
    tFIDFDataFrame.columns = vectorizer.get_feature_names()
    tFIDFSorted = numpy.argsort(tfidf.toarray(), axis=1)[:, -3:]
    for i in range(len(corpus)):
        q = questions[i]
        id = key_list[i]
        for w in tFIDFDataFrame.columns[tFIDFSorted][i]:
            if w == "wumpus":
                continue
            if w not in result_dict:
                result_dict[w] = []
            if id not in result_dict[w]:
                result_dict[w].append(id)
    course_dict[course_name] = result_dict
    return result_dict


def del_course(course):
    if course in course_dict:
        del course_dict[course]


def get_answer(course_name, word):
    result_dict = get_word_dict(course_name)
    if result_dict is None:
        return None
    else:
        id_list = []
        word_list = word.split(" ")
        for w in word_list:
            if w in result_dict:
                id_list.extend(result_dict[w])
        if len(id_list) > 0:
            result = Counter(id_list)
            d = sorted(result.items(), key=lambda x: x[1], reverse=True)
            return d[0][0]
    return None



if __name__=="__main__":
    result_dict = get_word_dict('COMP9414')
    print(result_dict)