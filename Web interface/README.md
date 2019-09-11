Gateway layer：
flask

Data layer：
mongodb


db collection:
chat

db tables:
1 question table: record chalk robot unsolved questions 
  
  _id: parimary key id
  content: question
  status: 0：unsolved，1：sovled
  email: email address
  
2 course table: record outline of course
  
  _id: primary key id
  course: course name
  content: outline 

3 record table: record solved questions and their answers
  
  _id : primary key id
  course: course name
  question: questions
  answer: answers
  
api：
   
    1 url: /hi
      Test website launch
      method: get
      Request：none
      Return：
      Show topics list
      
    
    2 url: /answer
      Teachers to answer questions
      method : post
      Request: question_id+answer
      Return: 
      
    3 url : /leave_message
      Students leave questions
      method : post
      Request: question and email address
      
    4 url: /show/questions
      Show unsolved questions for teachers
      method:get
      Request：none
      Return: Questions list
    
    5 url: /send_message
      Students chat with chalk robot
      method: post
      Request： message 
      Return：none
     
    6 url :/webhook
      dialogflow api

          
Background preprocessing
    Process messages.json, clean up and match the imported record table
    Process the course data, process it, and import it into the course table

Background processing
   Access dialogflow, extract intent, use sklearn to extract tfidf, keyword, search
    
  

