from pymongo import MongoClient
from bson.objectid import ObjectId

conn = MongoClient('localhost', 27017)
db = conn.chat
question_t = db.question


def insert_question(q):
    question_t.insert_one(q)

def get_question_by_status():
    result_list = question_t.find({'status': 0})
    data = []
    for r in result_list:
        data.append({'id': str(r['_id']), 'Question': r['content']})
    return data

def get_question_by_id(id):
    result = question_t.find_one({'_id': ObjectId(id)})
    if result and result['email'] and result['content']:
        course = ""
        if 'course' in result:
            course = result['content']
        return result['content'], result['email'], course
    else:
        return None, None

def update_status(id):
    question_t.update_one({'_id': ObjectId(id)}, {"$set":{'status': 1}})


if __name__ == "__main__":
    # seq 0
    q = {
        "content": "How do I initialize the weights when I train a deep neural network?",
        "status": 0,
        "email":'526064395@qq.com'
    }
    insert_question(q)

    #seq 1
    #print(get_question_by_status())

    #seq 2
    #print(get_question_by_id('5d26ed28a86a2257954a1dfb'))

    #seq 3
    #update_status('5d26ed28a86a2257954a1dfb')
