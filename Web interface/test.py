from flask import Flask, request, jsonify
from flask_restplus import Api, Resource, fields
from dbUtil.questionDBUtil import insert_question, get_question_by_status, update_status, get_question_by_id
from dbUtil.courseDBUtil import find_course_by_course
from dbUtil.recordDBUtil import search_by_id, insert_record
import dialogflow
from controller.search import get_answer, del_course
from util.tool import send_email
import os
from util.timeUtil import local_time


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="ChalkRobot9900-24e64d2180c4.json"


app = Flask(__name__)
api = Api(app)

@api.route("/hi")
class Hello(Resource):
    def get(self):
        return "hello world", 200

name_model = api.model('model', {'name': fields.String(required=True), 'password': fields.String})

@api.route("/webhook")
class Webhook(Resource):
    def post(self):
        try:
            data = request.get_json(silent=True)
            print(data)
            course = None
            outline = None
            if "course" in data['queryResult']['parameters']:
                course = data['queryResult']['parameters']['course']
                if len(course) > 0:
                    course = "comp" + course
            if 'outline' in data['queryResult']['parameters']:
                outline = data['queryResult']['parameters']['outline']
                outline = outline.lower()
            if (outline is None or len(outline) == 0) and (course is not None and len(course) > 0):
                content = find_course_by_course(course)
                if content:
                    reply = {
                        "fulfillmentText": content,
                        "questionType": 1
                    }
            elif len(outline) > 0 and (course is None or len(course) == 0):
                id = get_answer("all", outline)
                if id is not None:
                    response = search_by_id(id)
                else:
                    response = "What is the course?"
                reply = {
                    "fulfillmentText": response,
                    "questionType": 1
                }
            else:
                id = get_answer(course, outline)
                if id is not None:
                    response = search_by_id(id)
                else:
                    response = "Sorry, I don't understand what you said."
                reply = {
                    "fulfillmentText": response,
                    "questionType": 1
                }
            return jsonify(reply)
        except Exception:
            reply = {
                "fulfillmentText": "Sorry, I don't understand what you said.",
                "questionType": 1
            }
            return jsonify(reply)


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        #print("----------response---------")
        #print(response)
        type = 0
        if response.query_result.intent.display_name in ['course', 'outline']:
            type = 1
        return response.query_result.fulfillment_text,type


l_message_model = api.model('l_message_model', {
    'message': fields.String(required=True),
    })
@api.route("/send_message")
class Message(Resource):

    @api.expect(l_message_model)
    def post(self):
        message = api.payload['message']
        project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
        fulfillment_text, questionType = detect_intent_texts(project_id, "unique", message, 'en')
        response_text = {"message": fulfillment_text, "questionType": questionType}

        return jsonify(response_text)


message_model = api.model('message_model', {
    'course': fields.String(required=True),
    'question': fields.String(required=True),
    'email': fields.String(required=True),
    })

@api.route("/leave_message")
class Leave(Resource):
    @api.expect(message_model)
    def post(self):
        course =  api.payload['course']
        question = api.payload['question']
        email = api.payload['email']
        if question and email:
            q = {
                "course": course,
                "content": question,
                "status": 0,
                "email": email
            }
            insert_question(q)
            return {}, 200
        else:
            return {'msg': 'error input'}, 402

@api.route("/show/questions")
class Question(Resource):
    def get(self):
        question_list = get_question_by_status()
        return {'questions': question_list}


answer_model = api.model('answer_model', {
    'question_id': fields.String(required=True),
    'answer': fields.String(required=True),
    })
@api.route("/answer")
class Answer(Resource):
    @api.expect(answer_model)
    def post(self):
        question_id = api.payload['question_id']
        answer = api.payload['answer']
        if question_id and answer:
            update_status(question_id)
            question, email, course = get_question_by_id(question_id)
            q = {
                "course": course,
                "question": question,
                "answer": answer
            }
            insert_record(q)
            del_course(course)
            if question and email:
                content = "Dear student, you have a new response for your question from Chalk Robot.\n\nQuestion: " \
                          + question + "\nAnswer: " + answer +"\n\nDelivered by Chalk Robot " + local_time()
                send_email(email, content)
        return {}, 200


if __name__ == '__main__':
    app.run(debug=True)
