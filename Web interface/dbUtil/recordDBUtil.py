from pymongo import MongoClient
from bson.objectid import ObjectId

conn = MongoClient('localhost', 27017)
db = conn.chat
r_table = db.record


def insert_record(q):
    r_table.insert_one(q)

def search_by_course(course):
    key_list = []
    questions = []
    result_list = r_table.find({'course': course})
    for r in result_list:
        questions.append(r["question"])
        key_list.append(str(r["_id"]))
    return questions, key_list


def search_by_id(id):
    result_list = r_table.find({'_id': ObjectId(id)})
    for r in result_list:
        return r["answer"]


def search_all():
    key_list = []
    questions = []
    result_list = r_table.find()
    for r in result_list:
        questions.append(r["question"])
        key_list.append(str(r["_id"]))
    return questions, key_list


if __name__=='__main__':
    d = {
        "course": "comp9414",
        "question": "",
        "answer": ""
    }
    insert_record(d)