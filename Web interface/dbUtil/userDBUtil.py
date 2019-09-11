from pymongo import MongoClient
from util.tool import create_salt, create_md5

conn = MongoClient('localhost', 27017)
db = conn.chat
userInfo = db.userInfo

def insert_user(user):
    userInfo.insert_one(user)

def get_user_by_name(name):
    return userInfo.find_one({'name':name})


if __name__ == "__main__":
    student = {
        "name": "tom",
        "password": "123456",
        "identity": "student"
    }
    student['salt'] = create_salt()
    student['password'] = create_md5(student['password'], student['salt'])
    insert_user(student)

    teacher = {
        "name": "Mike",
        "password": "654321",
        "identity": "teacher"
    }
    teacher['salt'] = create_salt()
    teacher['password'] = create_md5(teacher['password'], teacher['salt'])
    insert_user(teacher)