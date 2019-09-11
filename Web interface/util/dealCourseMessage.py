import json
import os
from dbUtil.recordDBUtil import insert_record
from dbUtil.courseDBUtil import insert_course
import csv

def get_course():
    path_name = "./data/course"
    fileList = os.listdir("./data/course")
    course_dict = {}
    for file_name in fileList:
        with open(path_name+"/"+file_name, "r", encoding='utf-8') as f:
            id = file_name.split('.')[0]
            content = f.read()
            course_dict[id] = content
    return course_dict

# def read_message():
#     tmp = ["2.json", "6.json", "7.json", "17.json"]
#     course_dict = get_course()
#     json_files = os.listdir("./data/j")
#     for json_file in json_files:
#         if json_file in tmp or not json_file.endswith(".json"):
#             continue
#         print(json_file)
#         with open("./data/json/"+json_file, "r", encoding='utf-8') as f:
#             s = f.read().encode('utf-8')
#             data_list = json.loads(s)
#             for data in data_list:
#                 course = data["course"].split()[0]
#                 if course in course_dict:
#                     q = {"course": course,"mesg_id":data["mesg_id"],"message": data["message_body"]}
#                     if "parent_id" in data:
#                         q["parent_id"] = data["parent_id"]
#                     insert_record(q)
#                     #print(q)


def read_csv():
    csv_files = os.listdir("./data/9414")
    for name in csv_files:
        with open('./data/9414/'+name, 'r')as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                q = {
                    "course": "comp9414",
                    "question": row[0].strip("?").lower(),
                    "answer": row[1]
                }
                insert_record(q)

def read_messaga_info():
    question_dict = {}
    answer_dict = {}
    with open("./data/messages.json", "r") as f:
        content = ""
        for line in f:
            line = line.strip("\n")
            line = line.replace("\\0", '').replace("\\x"," ").replace('\l',"")
            if line not in ['[', ']']:
                content += line
            if line == '},':
                content = content.strip(",")
                try:
                    data = json.loads(content)
                    course = data["course"].split()[0].lower()
                    q = {"course": course, "mesg_id": data["mesg_id"], "message": data["message_body"]}
                    if "parent_id" in data:
                        q["parent_id"] = data["parent_id"]
                    else:
                        q["message"] = q["message"].lower()
                        q["parent_id"] = None
                    if q["parent_id"] is not None:
                        if q["parent_id"] in question_dict:

                            d = {
                                "course": course,
                                "question": question_dict[q["parent_id"]]["message"],
                                "answer": q["message"]
                             }
                            insert_record(d)
                        else:
                             answer_dict[q["parent_id"]] = q
                    else:
                        if q["mesg_id"] in answer_dict:
                            d = {
                                "course": course,
                                "question": q["message"],
                                "answer": answer_dict[q["mesg_id"]]["message"]
                            }
                            insert_record(d)
                        else:
                            question_dict[q["mesg_id"]] = q
                except Exception as e:
                    print(e)
                    print(content)
                content = ""
        print("finish")

if __name__=="__main__":

    # 导入 course
    course_dict = get_course()
    for key in course_dict.keys():
        q = {"course": key.lower(), "content": course_dict[key]}
        insert_course(q)
    # 处理 message 信息
    read_messaga_info()
    l = read_csv()
