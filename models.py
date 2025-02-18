from flask_sqlalchemy import SQLAlchemy
from app import app
db = SQLAlchemy()
db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username  = db.Column(db.String(), unique = True, nullable = False)
    password =  db.Column(db.String(), nullable = False)
    fullName =  db.Column(db.String(), nullable = False)
    Qualification =  db.Column(db.String(), nullable = False)
    DOB = db.Column(db.date)
    is_admin = db.Column(db.String(), unique = True, nullable = False)
    scores = db.relationship('Score', backref = 'user', lazy= True)


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name  = db.Column(db.String(), unique = True, nullable = False)
    description =  db.Column(db.String(), nullable = False)
    chapters = db.relationship('Chapter', backref = 'subject', lazy = True)
    
class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name  = db.Column(db.String(), unique = True, nullable = False)
    description =  db.Column(db.String(), nullable = False)    
    chap_sub_id = db.Column(db.Integer,db.foreign_key('subject.id'), nullable = False)
    db.relationship('Quiz', backref = 'chapter', lazy = True)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    chapter_id = db.Column(db.Integer,db.foreign_key('Chapter.id'), nullable = False)
    date_of_quiz = db.Column(db.date, nullable = False)
    time_duration = db.Column(db.String(), nullable = False)
    remarks =  db.Column(db.String(), nullable = False)
    db.relationship('Questions', backref = 'quiz', lazy = True)
    db.relationship('Score', backref= 'quiz', lazy = True)


class Questions(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    quiz_id = db.Column(db.Integer, db.Foreign_key('quiz.id'), nullable = False)
    question_statement = db.Column(db.String(), unique = True, nullable = False)
    option_1 =  db.Column(db.String(), nullable = False)
    option_2 =  db.Column(db.String(), nullable = False)
    option_3 =  db.Column(db.String(), nullable = False)
    option_4 =  db.Column(db.String(), nullable = False)
    


class Scores(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    quiz_id  =  db.Column(db.Integer, db.Foreign_key('Quiz.id'), nullable = False)
    user_id  = db.Column(db.Integer, db.Foreign_key('User.id'), nullable = False)
    time_stamp_of_attempt =  db.Column(db.String(), nullable = False)
    total_scored =  db.Column(db.String(), nullable = False)
    


'''User - Can attempt any quiz of its choice
User Registration and Login
Each user may have:
id - primary key
Username (email)
Password
Full Name
Qualification
DOB
To be able to choose the subject as well as the chapter name
Start the quiz
View the quiz scores
Terminologies

User: The user will register/login and attempt any quiz of his/her interest.


Admin: The superuser with full control over other users and data. Registration is not allowed for the admin: The admin account must pre-exist in the database when the application is initialized.


Subject: The field of study in which the user wishes to give the quiz. The admin will be creating one or many subjects in the application. Every subject can possibly have the following fields:


id - primary key
Name
Description
etc: Additional fields (if any)

Chapter: Each subject can be subdivided into multiple modules called chapters. The possible fields of a chapter can be the following:

id - primary key
Name
Description
etc: Additional fields (if any)

Quiz: A quiz is a test that is used to evaluate the user’s understanding of any particular chapter of any particular subject. A test may contain the following attributes:


id - primary key
chapter_id (foreign key-chapter)
date_of_quiz
time_duration(hh:mm)
remarks (if any)
etc: Additional fields (if any)
Questions: Every quiz will have a set of questions created by the admin. Possible fields for a question include:

id - primary key
quiz_id (foreign key-quiz)
question_statement
Option1, option2, … etc.
etc: Additional fields (if any)

Scores: Stores the scores and details of a user's quiz attempt. Possible fields for scores include:

id - primary key
quiz_id (foreign key-quiz)
user_id (foreign key-user)
time_stamp_of_attempt
total_scored
etc: Additional fields (if any)    '''