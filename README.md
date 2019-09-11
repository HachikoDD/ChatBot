# Chalk tutor conversational agent

## Report
Proposal: https://docs.google.com/document/d/1R5K8abM9D27iFqOGSX3bSimySWFwfFzuqTpdYE3OAO8/edit?usp=sharing

Please find PDF Version of Proposal here：[PDF Version of Proposal](https://github.com/unsw-cse-comp3900-9900/capstone-project-not-missing-one/blob/master/Chalk%20Proposal/Thesis_proposal.pdf)

Dialogflow: https://dialogflow-python-client-v2.readthedocs.io/en/latest/


## Report

Final report: https://docs.google.com/document/d/1biG_9fmoG-GVKnTee-yN6GfYXSnV8s6M3o0fDjo3VKU/edit?usp=sharing

Please find PDF Version of Proposal here：[PDF Version of Final Report](https://github.com/unsw-cse-comp3900-9900/capstone-project-not-missing-one/blob/master/Chalk%20Report/Thesis_proposal.pdf)

### Trello：[Trello Invitation link](https://trello.com/invite/b/9DNZpnYx/6324c3fa9c8f3984867819f5635c9058/9900-not-missing-one)

# Chalk
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue)](https://www.python.org/downloads/release/python-370/)
[![flask](https://img.shields.io/badge/flask-1.1.1-blue)](https://github.com/pallets/flask)
[![bootstrap](https://img.shields.io/badge/bootstrap-4.3.1-yellow)](https://getbootstrap.com/)
[![jquery](https://img.shields.io/badge/jQuery-4.3.1-yellow)](https://jquery.com/)
[![wangeditor](https://img.shields.io/badge/flask-3.1.1-yellow)](http://www.wangeditor.com/)
[![layer](https://img.shields.io/badge/layer-3.3.1-yellow)](https://layer.layui.com/)

A performing well and intelligent chat robot will not only improve the learning efficiency of students but also reduce the burden on teachers. But today most chatbots don't have an appropriate feedback mechanism. In this project, we aim to build a chat robot which has a self-learning mechanism. The backend will distinguish course-related questions from daily greetings questions. If the student enters a course-related question, the dialog responded by chatbot will have like or dislike button. If the student doesn’t like the answer, he can leave his email, and waiting for further help. The unsatisfied answer will be forwarded to the management page, the teacher will be able to update the answer. The student will get update answer by email, and the chatbot database also will be updated. If another student asks a similar question, we the new answer will be provided.

An example of typical input would be something like this:

> **user:** Hi  
> **chalk:**  Good day! What can I do for you today?  
> **user:** What is COMP9414？  
> **chalk:** COMP9414 Artificial Intelligence Overview of Artificial Intelligence. Topics include: the representation of knowledge, search techniques,problem solving, machine learning, expert systems, natural language understanding, computer vision andan Artificial Intelligence programming language  Prolog or LISP. Students may be requiredto submit simple Art ificial Intelligence programs, or essays on an aspectof AI, for assessment, in areas such as robotics, computer vision, naturallanguage processing, and machine learning.

## How to run

- To start MongoDB using all defaults, issue the following command at the system shell:
```
mongod
```
- Then open a new shell and issue the following command:
```
mongo
```
- Run file dealCourseMessage.py, the file path is Web interface/util/dealCo-urseMessage.py.
```
python dealCourseMessage.py
```
- Run file app.py, the file path is Web interface/app.py
```
python app.py
```
- Download and Startup ngrok
```
./ngrok http localhost:5000
```
- Then we need to copy this URL as below because this link will change every time we start ngrok.

    ![ngrok](https://i.ibb.co/F6j107H/m5.png)

- Paste it into the fulfillment sitting page of the Dialogflow, we will use it later at Twitter Support as well.
  - **Google account:**

  - **Password:**

    ![ngrok2](https://i.ibb.co/PxHXFFj/m6.png)

- Finallny, you are ready to go

    ![chat](https://i.ibb.co/7JVDGmm/homepage-chat.png)
