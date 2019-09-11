import sys

from flask import Flask, flash, request, url_for, redirect, render_template, session, jsonify
from werkzeug.security import check_password_hash
from util.tool import create_md5, generate_token, certify_token, send_email, create_salt
from dbUtil.questionDBUtil import insert_question, get_question_by_status, update_status, get_question_by_id
from dbUtil.courseDBUtil import find_course_by_course
from dbUtil.recordDBUtil import search_by_id, insert_record
from dbUtil.userDBUtil import get_user_by_name, insert_user
from flask_login import LoginManager, login_user, UserMixin, login_required, logout_user, current_user
import dialogflow
from controller.search import get_answer, del_course
from util.timeUtil import local_time
import os
import json
import time

app = Flask(__name__)
app.secret_key = "super secret key"
login_manager = LoginManager()

# Login 初始化
login_manager.login_view = 'login'
login_manager.login_message = 'please login!'
login_manager.session_protection = 'strong'
app.config['SECRET_KEY'] = '1234567'
login_manager.init_app(app)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="ChalkRobot9900-24e64d2180c4.json"

def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        course = response.query_result.parameters.fields['course'].string_value
        course = "comp" + course
        type = 0
        if response.query_result.intent.display_name in ['course', 'outline']:
            type = 1
        return response.query_result.fulfillment_text, type, course

class User():

    def __init__(self, username):
        self.username = username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)

@app.route("/webhook", methods=['POST'])
def webhook():
    try:
        data = request.get_json(silent=True)
        # print(data)
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
            content = keep_first_N(content)
            if content:
                reply = {
                    "fulfillmentText": content,
                    "questionType": 1,
                }
        elif len(outline) > 0 and (course is None or len(course) == 0):
            id = get_answer("all", outline)
            if id is not None:
                response = search_by_id(id)
                response = keep_first_N(response)
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
                response = keep_first_N(response)
            else:
                response = "Sorry, I don't understand what you said."
            reply = {
                "fulfillmentText": response,
                "questionType": 1
            }
        # print(reply)
        return jsonify(reply)
    except Exception:
        reply = {
            "fulfillmentText": "Sorry, I don't understand what you said.",
            "questionType": 1
        }
        return jsonify(reply)

@app.route("/")
def home():
    return render_template("homepage.html")


# @app.route("/send_message", methods=['POST'])
# def send_message():
#     # userText = request.args.get('msg')
#     # return str(english_bot.get_response(userText))
#     return render_template("login.html")

@app.route("/send_message", methods=['POST'])
def send_message():
    data = request.get_json()
    message = data["question"]
    # print(message, file=sys.stdout)
    # message = userText
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text, questionType, course = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = {"message": fulfillment_text, "questionType": questionType, "course": course}
    return jsonify(response_text)

def keep_first_N(fulfillment_text):
    the_first_N = 0;
    for i in fulfillment_text:
        if(i == '\n'):
            break
        else:
            the_first_N = the_first_N + 1
    fulfillment_text = fulfillment_text.replace("\n", "")
    fulfillment_text = fulfillment_text[:the_first_N] + '\n' + fulfillment_text[the_first_N:]
    return fulfillment_text

@app.route("/leave_message",  methods=['POST'])
def Leave():
    data = request.get_json()
    question = data["question"]
    email = data["email"]
    course = data["course"]
    if question and email:
        q = {
            "course": course,
            "content": question,
            "status": 0,
            "email": email
        }
        insert_question(q)
        return "1"
    else:
        return "0"

@app.route("/show/questions", methods=['GET'])
def Question():
    question_list = get_question_by_status()
    return json.dumps(question_list)

@app.route("/answer", methods=['POST'])
def Answer():
    if request.method == 'POST':
        data = request.get_json()
        question_id = data["question_id"]
        answer = data["answer"]
        print(question_id, file=sys.stdout)
        print(answer, file=sys.stdout)
        # question_id = app.payload['question_id']
        # answer = app.payload['answer']
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
                content = "<br><h5>*** This is an automatically generated email, please do not reply ...</h5>\
                            <h3>Chalk Auto Response</h3>\
                            <p>Dear student:</p>\
                            <pre>You have a new response for your question at Chalk Robot.</pre><br>\
                            <pre style=padding-left: 30px;>Question:</pre>\
                            <pre style=padding-left: 60px;>"+question+"</pre>\
                            <br>\
                            <pre style=padding-left: 30px;>Answer:</pre>\
                            <pre style=padding-left: 60px;>"+answer+"</pre>\
                            <br>\
                            <pre>Chalk Robot " + local_time() + "</pre>"
                send_email(email, content)
        return "1"
    return "0"

@login_manager.user_loader
def user_loader(user_name):
    user = get_user_by_name(user_name)
    return User(user['name'])

@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['username']
        password = request.form['password']
        remember = request.form['remember']
        token = generate_token(user_name)
        user = get_user_by_name(user_name)
        if user:
            salt = user['salt']
            pwd = create_md5(password, salt)
            next = request.args.get('next')
            if pwd == user['password']:
                user_obj = User(user_name)
                login_user(user_obj, remember=remember)
                # session['user_token'] = token
                # return 'You are logged in as ' + user_name
                return redirect(next or url_for('management'))
            else:
                return '<h1> Wrong Password <h1>'
        else:
            return render_template("login.html")
    return render_template("login.html")

@app.route("/register", methods=['POST'])
def register():
    if request.method == 'POST':
        user_name = request.form['username']
        password = request.form['password']
        user = get_user_by_name(user_name)
        if not user:
            user = {
                "name": user_name,
                "password": password,
                "identity": "student"
            }
            user['salt'] = create_salt()
            user['password'] = create_md5(user['password'], user['salt'])
            insert_user(user)
            return redirect(url_for('management'))
        flash('User name already exists.')
        return redirect(url_for('register'))
    return render_template("register.html")

@app.route("/management", methods=['GET', 'POST'])
@login_required
def management():
    return render_template("management.html", name = current_user.username)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/answer_window", methods=['GET', 'POST'])
def answer_window():
    return render_template("answer.html")
if __name__ == '__main__':
    app.run()
