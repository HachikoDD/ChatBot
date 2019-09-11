from pymongo import MongoClient

conn = MongoClient('localhost', 27017)
db = conn.chat
topic_t = db.topic


def insert_topic(t):
    topic_t.insert_one(t)



def get_all_topic():
    result_list = topic_t.find()
    data = []
    for r in result_list:
        data.append({'id': str(r['_id']), 'topic': r['topic_word']})
    return data


if __name__ == "__main__":
    # t = {
    #     "topic_word": "course",
    # }
    # insert_topic(t)
    print(get_all_topic())