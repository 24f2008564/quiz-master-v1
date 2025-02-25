#from flask_sqlalchemy import SQLAlchemy
from .database import db

#db = SQLAlchemy(app)



class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username  = db.Column(db.String(), unique = True, nullable = False)
    password =  db.Column(db.String(), nullable = False)
    fullname =  db.Column(db.String(), nullable = False)
    qualification =  db.Column(db.String(), nullable = False)
    DOB = db.Column(db.DateTime)
    is_admin = db.Column(db.String(), unique = True, nullable = False, default = False)
    scores = db.relationship('Scores', backref = 'user', lazy= True)
    subjects = db.relationship('Subject', backref = 'user', lazy = True)

class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name  = db.Column(db.String(), unique = True, nullable = False)
    description =  db.Column(db.String(), nullable = False)
    chapters = db.relationship('Chapter', backref = 'subject', lazy = True)
    user_subject = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

class Chapter(db.Model):
    __tablename__ = 'chapter'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name  = db.Column(db.String(), unique = True, nullable = False)
    description =  db.Column(db.String(), nullable = False)    
    subject_id = db.Column(db.Integer,db.ForeignKey('subject.id'), nullable = False)
    quizzes = db.relationship('Quiz', backref = 'chapter', lazy = True)

class Quiz(db.Model):
    __tablename__ = 'quiz'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    chapter_id = db.Column(db.Integer,db.ForeignKey('chapter.id'), nullable = False)
    date_of_quiz = db.Column(db.Date, nullable = False)
    time_duration = db.Column(db.String(), nullable = False)
    remarks =  db.Column(db.String(), nullable = False)
    questions = db.relationship('Question', backref = 'quiz', lazy = True)
    scores = db.relationship('Scores', backref= 'quiz', lazy = True)


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable = False)
    question_statement = db.Column(db.String(), unique = True, nullable = False)
    option_1 =  db.Column(db.String(), nullable = False)
    option_2 =  db.Column(db.String(), nullable = False)
    option_3 =  db.Column(db.String(), nullable = False)
    option_4 =  db.Column(db.String(), nullable = False)
    


class Scores(db.Model):
    __tablename__ = 'scores'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    quiz_id  =  db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable = False)
    user_id  = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    time_stamp_of_attempt =  db.Column(db.DateTime, nullable = False)
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