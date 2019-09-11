from pymongo import MongoClient

conn = MongoClient('localhost', 27017)
db = conn.chat
c_table = db.course


def insert_course(q):
    c_table.insert_one(q)


def find_course_by_course(course):
    result_list = c_table.find({'course':course})
    for r in result_list:
        return r['content']




