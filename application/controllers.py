from flask import Flask, render_template, redirect, request, url_for,flash, jsonify
from flask import current_app as app
from .models import *
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')

admin = {
    "username": "24f2008564@ds.study.iitm.ac.in",
    "password": "kshitijiitmadras",

}
#login for admin and user
@app.route("/", methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        ext_user = User.query.filter_by(username = uname, password = pwd).first()
        
        if ext_user and ext_user.is_admin == 1:
            subjects = Subject.query.all()
            #chapters = Chapter.query.all()
            return render_template("admin_dashbord.html", subjects = subjects)#, ext_user = ext_user)
        elif ext_user:
            quizzes = Quiz.query.all()
            return render_template("user_dashboard.html", ext_user = ext_user, quizzes = quizzes)
        else:
            return render_template("login.html", msg = "Invalid user credentials")
    
    return render_template("login.html", msg="")
   


# registration form
@app.route("/register", methods = ['GET','POST'])
def register():
    
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['Password']
        fullname  = request.form['Fullname']   
        dob = request.form['DOB']
        dob_obj = datetime.strptime(dob, '%Y-%m-%d').date()
        if not User.query.filter_by(username = username).first():
            new_user = User(username = username, password = password, fullname = fullname,  DOB=dob_obj)
            
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            #flash("user already exist")
            return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template('register.html')


# go to admin 
@app.route("/admin")
def admin():
    subjects = Subject.query.all()
    #exit_user = User.query.filter_by(is_admin = True).first()
    #return render_template("admin_dashbord.html", subjects = subjects, exit_user = exit_user)  
    return render_template("admin_dashbord.html", subjects = subjects)

#@app.route("/api/subjects", methods = ['GET'])
#def get_subjects():
#    subjects = Subject.query.all()
#    s_list = []
#    for subject in subjects:
#        s_list.append({"id": subject.id, "name": subject.name, "descrition": subject.description, "chapters":[chapter.name for chapter in subject.chapters]})
#    return jsonify(s_list)
#
#
@app.route("/api/subjects", methods = ['GET'])
def get_subjects():
    subjects = Subject.query.all()
    s_list = []
    for subject in subjects:
        s_list.append({"id": subject.id, "name": subject.name, "descrition": subject.description, "chapters":[chapter.name for chapter in subject.chapters]})
    return jsonify(s_list)



# Go to userdashboard
@app.route("/user_dashboard/<int:user_id>")
def user_dashboard(user_id):
    ext_user = User.query.filter_by(id = user_id).first()
    quizzes = Quiz.query.all()
    msg = request.args.get('msg', '')
    return render_template("user_dashboard.html", ext_user = ext_user, quizzes = quizzes, msg = msg)


@app.route("/search", methods= ['GET'])
def search():
    query = request.args.get('s','')
    if not query:
        return render_template("search.html", query= query)
    elif query.lower() == 'subjects' or query.lower()  == 'subject':
        subjects = Subject.query.all()
        return render_template("results.html", subjects = subjects, quizzes = "", users = "", questions ="",  query =query)
    elif query.lower() == 'quiz' or query.lower()  == 'quizzes':
        quizzes = Quiz.query.all()
        return render_template("results.html", subjects ="", quizzes = quizzes, users = "", questions ="",  query =query)
    elif query.lower() == 'users' or query.lower() == 'user':
        users=  User.query.all()
        return render_template("results.html", subjects= "", quizzes = "", users = users, questions ="",  query =query)
    elif query.lower() == 'questions':
        questions  = Question.query.all()
        return render_template("results.html", subjects = "", quizzes = "", users = "", questions = questions,  query =query)
    
    
    subjects = Subject.query.filter(Subject.name.ilike(f"%{query.lower()}%")).all()
    #chapters = Chapter.query.filter(Chapter.name.ilike(f"{query}")).all()
    quizzes = Quiz.query.filter(Quiz.name.ilike(f"{query.lower()}")).all()
    users = User.query.filter(User.fullname.ilike(f"{query.lower()}")).all()

    return render_template("results.html", subjects = subjects, quizzes = quizzes, users  = users, questions = "", query = query)

@app.route("/user/search")
def usersearch():
    search_word = request.args.get('us', '')
    subjects = Subject.query.all()
    quizzes = Quiz.query.all()
    if search_word == 'subjects':
        quizzes = None
    elif search_word == 'quizzes':
        subjects = None    
    return render_template("userresults.html", subjects = subjects, quizzes = quizzes, search_word = search_word)
    
#ADD SUBJECT      
@app.route('/Addsubject', methods = ['GET','POST'])
def addsubject():
    if request.method == 'POST':
        sub_name = request.form['subject']
        describe = request.form['Description']
        new_sub = Subject.query.filter_by(name = sub_name).first()
 #       subjects = Subject.query.all()
        if not new_sub:
            new_sub = Subject(name = sub_name, description = describe)
            db.session.add(new_sub)
            db.session.commit()
            return redirect(("/admin"))
        
    return render_template("addsubject.html", message = "")

#DELETE SuBJECT
@app.route('/subject/<int:subject_id>/delete/', methods = ['GET','POST'])
def deletesubject(subject_id):
    subject = Subject.query.filter_by(id = subject_id).first()
    if subject:
        db.session.delete(subject)
        db.session.commit()
        return redirect(url_for('admin'))
    
#EDIT SUBJECT
@app.route('/subject/<int:subject_id>/edit/', methods = ['GET','POST'])
def editsubject(subject_id):
    subject = Subject.query.filter_by(id = subject_id).first()
    if request.method == 'POST': 
        if subject:
            name = request.form.get('subject')
            description = request.form.get('Description')
            subject.name = name
            subject.description = description
            db.session.commit()
            return redirect(url_for("admin"))
    return render_template("updatesubject.html", subject = subject)    


#ADD CHAPTER
@app.route("/Addchapter/<int:subjectid>/", methods = ['GET','POST'])
def addchapter(subjectid):
    if request.method == 'POST':
        name = request.form['chaptername']
        description = request.form['Description']

        subject = Subject.query.filter_by(id = subjectid).first()
        if Chapter.query.filter_by(name = name).first():
            return redirect("url_for('addchapter')") 
        new_chapter = Chapter(name = name, description = description, subject_id = subject.id)
        db.session.add(new_chapter)
        db.session.commit()
        return redirect(url_for("admin"))


    if request.method == 'GET':
        subject = Subject.query.filter_by(id = subjectid).first()

        if subject:
            return render_template("addchapter.html", subject = subject)    
        else:
            return redirect(url_for("addsubject"))

# EDIT CHAPTER        
@app.route("/chapter/<int:chapter_id>/edit/", methods = ['GET','POST'])
def editchapter(chapter_id):
    chapter = Chapter.query.filter_by(id = chapter_id).first()
    fsubject  = Subject.query.filter_by(id = chapter.subject_id).first() 
    if request.method == 'POST':
            chapter.name = request.form.get('chaptername')
            chapter.description = request.form.get('description')
            subjectname  = request.form.get('subjectname')
            subject1 = Subject.query.filter_by(name = subjectname).first()
            if subject1:
              chapter.subject_id = subject1.id
              db.session.commit()
              return redirect(url_for('admin'))
            else:
                return render_template("addsubject.html", message = "Subject does not exist. First Add subject")
                
            
    return render_template("updatechapter.html", chapter = chapter, subject = fsubject)

#DELETE CHAPTER
@app.route('/chapter/<int:chapter_id>/delete/', methods = ['GET','POST'])
def deletechapter(chapter_id):
    chapter = Chapter.query.filter_by(id = chapter_id).first()
    if chapter:
        db.session.delete(chapter)
        db.session.commit()
        return redirect(url_for('admin'))

#ADD QUIZ      
@app.route("/quiz/<int:chapter_id>/", methods = ['GET','POST'])
def addquiz(chapter_id):
    chapter = Chapter.query.filter_by(id = chapter_id).first()
    if request.method == 'POST':
        name = request.form.get('name')
        date_obj = request.form.get('date')
        date = datetime.strptime(date_obj, '%Y-%m-%d').date()
        duration = request.form.get('duration')
        remarks = request.form.get('remarks') or None
        new_quiz= Quiz(name = name, chapter_id = chapter_id ,date_of_quiz = date, time_duration = duration, remarks = remarks)
        db.session.add(new_quiz)
        db.session.commit()
        return redirect(url_for('quizmanagement', chapter_id = chapter.id))
    
    return render_template("addquiz.html", chapter = chapter)


#EDIT QUIZ
@app.route("/quiz/<int:quiz_id>/edit",  methods = ['GET','POST'])
def editquiz(quiz_id):
    quiz = Quiz.query.filter_by(id = quiz_id).first()
    chapter = Chapter.query.filter_by(id = quiz.chapter_id).first()
    #subject = Subject.query.filter_by(id = chapter.subject_id).first()
    if request.method == 'POST':
        quiz.name = request.form.get('name')  
        quiz.time_duration = request.form.get('time_duration')
        date_obj = request.form.get('date')
        quiz.date_of_quiz = datetime.strptime(date_obj, '%Y-%m-%d').date()
        quiz.remarks = request.form.get('remarks') or None
        db.session.commit()
        return redirect(url_for('quizmanagement', chapter_id = chapter.id))        
    return render_template("updatequiz.html", quiz =  quiz ,chapter = chapter)



#DELETE QUIZ
@app.route('/quiz/<int:quiz_id>/delete/', methods = ['GET','POST'])
def deletequiz(quiz_id):
    quiz = Quiz.query.filter_by(id = quiz_id).first()
    chapter= Chapter.query.filter_by(id = quiz.chapter_id).first()
    if quiz:
        db.session.delete(quiz)
        db.session.commit()
        return redirect(url_for('quizmanagement', chapter_id= chapter.id))
    else:
        return redirect(url_for('quizmanagement', mes = "Quiz does not exist"))
    
# get quizzes
@app.route("/api/quizzes/")
def getquizzes():
    quizzes = Quiz.query.all()
    qlist = []
    for quiz in quizzes:
        qlist.append({"id":quiz.id, "name":quiz.name , "date": quiz.date_of_quiz, "timeduration": quiz.time_duration})
    return jsonify(qlist)    


#Add question 
@app.route("/addquestion/<int:quiz_id>",  methods = ['GET','POST'])
def addquestion(quiz_id):
    quiz = Quiz.query.filter_by(id = quiz_id).first()
    if request.method == 'POST':
        question = request.form.get('question description')  
        question_title = request.form.get('question_title')
        option_1 = request.form.get('option 1')  
        option_2 = request.form.get('option 2')  
        option_3 = request.form.get('option 3')  
        option_4 = request.form.get('option 4')  
        correct_option = request.form.get('correct option')  
        new_question =  Question(question_title = question_title, question_statement = question, option_1=  option_1, option_2=  option_2,
        option_3=  option_3,option_4= option_4,correct_option = correct_option, quiz_id = quiz_id)                         
        db.session.add(new_question)
        db.session.commit()
        return redirect(url_for('questionmanagement', quiz_id = quiz_id))
    
    return render_template("addquestion.html", quiz = quiz)

#editquestion
@app.route("/question/<int:question_id>/edit",  methods = ['GET','POST'])
def editquestion(question_id):
    question = Question.query.filter_by(id = question_id).first()
    quiz = Quiz.query.filter_by(id = question.quiz_id).first()
    if request.method == 'POST':
        question.question_title = request.form.get('question_title')  
        question.question_statement = request.form.get('question description')
        question.option_1 = request.form.get('option 1')
        question.option_2 = request.form.get('option 2')
        question.option_3 = request.form.get('option 3')
        question.option_4 = request.form.get('option 4')
        question.correct_option = request.form.get('correct_option')
        db.session.commit()
        return redirect(url_for('questionmanagement', quiz_id = quiz.id))        
    return render_template("updatequestion.html", question =  question)
        
#DELETE QUESTION
@app.route('/question/<int:question_id>/delete/', methods = ['GET','POST'])
def deletequestion(question_id):
    question = Question.query.filter_by(id = question_id).first()
    quiz_id = question.quiz_id
    quiz = Quiz.query.filter_by(id = quiz_id).first()
    if question:
        db.session.delete(question)
        db.session.commit()
        return redirect(url_for('questionmanagement', quiz_id = quiz.id))
    else:
        return redirect(url_for('questionmanagement', quiz_id = quiz.id))

#questionmanagment
@app.route("/questionmanagement/<int:quiz_id>")
def questionmanagement(quiz_id):
    quiz = Quiz.query.filter_by(id = quiz_id).first()
    chapter = Chapter.query.filter_by(id = quiz.chapter_id).first()
    return render_template("questionmanagement.html", quiz = quiz, chapter = chapter)

@app.route("/quizmanagement/<int:chapter_id>") 
def quizmanagement(chapter_id):
    chapter= Chapter.query.filter_by(id = chapter_id).first()
    return render_template("quizmanagement.html", chapter = chapter)

# view quiz
@app.route("/view_quiz/<int:quiz_id>/<int:user_id>")
def view_quiz(quiz_id, user_id):
    quiz = Quiz.query.filter_by(id = quiz_id).first()
    chapter = Chapter.query.filter_by(id = quiz.chapter_id).first()
    subject =Subject.query.filter_by(id = chapter.subject_id).first()
    user = User.query.filter_by(id = user_id).first()
    return render_template("view_quiz.html", quiz = quiz, chapter = chapter, subject = subject, user= user)


#attempt quiz
@app.route("/start_quiz/<int:quiz_id>/<int:user_id>", methods = ['GET','POST'])
def startquiz(quiz_id, user_id):
    quiz = Quiz.query.filter_by(id = quiz_id).first()
    chapter = Chapter.query.filter_by(id = quiz.chapter_id).first()
    user = User.query.filter_by(id = user_id).first()
    questions = quiz.questions
    #scores = user.scores
    if request.method == "POST":
        
        score  = 0
        for question in questions:
            chosenoption = request.form.get(f'{question.id}')
            if chosenoption and int(chosenoption) == question.correct_option:
                score+=1
            else:
                continue
        
        new_score = Scores(quiz_id = quiz_id, user_id = user_id, totalscore = score, date = quiz.date_of_quiz)
        db.session.add(new_score)
        db.session.commit()
        return redirect(url_for('user_dashboard', user_id = user_id))    

    #for score in scores:
    #        if user_id == score.user_id and quiz_id == score.quiz_id:
    #           return redirect(url_for('user_dashboard', user_id = user_id, msg = "USER HAS ALREADY ATTEMPTED THE QUIZ") )
    current_time = datetime.now()
    if (current_time.date()) >= (quiz.date_of_quiz):
        return redirect(url_for('user_dashboard', user_id = user_id, msg = "Date to attempt quiz has already passed") )
    
    return render_template("quiz.html", quiz = quiz, chapter=  chapter, user_id = user_id)            



#scores
@app.route("/score/<int:user_id>")
def scores(user_id):
    user = User.query.filter_by(id = user_id).first()
    scores = user.scores
    return render_template("scores.html", user = user, scores = scores)


@app.route("/summary/admin/", methods = ['GET', 'POST'])
def summaryadmin():
    subjects = Subject.query.all()
    subjectsdict = {}
    scores = Scores.query.all()
    #for subject in subjects:
    #    if subject.name in subjectsdict.keys():
    #        continue
    #    subjectsdict[subject.name] = 0
    #scores  =  Scores.query.all()
    for score in scores:
        quiz_id = score.quiz_id
        chapter_id  = (Quiz.query.filter_by(id =  quiz_id).first()).chapter_id
        subject_id = (Chapter.query.filter_by(id = chapter_id).first()).subject_id
        subjectname = (Subject.query.filter_by(id = subject_id).first()).name
        if subjectname not in subjectsdict.keys():
            subjectsdict[subjectname] = 0
        elif subjectsdict[subjectname] < int(score.totalscore):
            subjectsdict[subjectname] = int(score.totalscore)
    
    labels = list(subjectsdict.keys())
    topscrores = list(subjectsdict.values())
    plt.bar(labels, topscrores, color = "blue")
    plt.title("top scores by subject")
    plt.xlabel("subject")
    plt.ylabel("topscores")
    plt.savefig("static/chart.png")
    return render_template("summary_admin.html" )


@app.route("/summary/user/<int:user_id>", methods = ['GET', 'POST'])
def summaryuser(user_id):
    subjects = Subject.query.all()
    subjectsdict = {}
    scores = Scores.query.filter_by(user_id = user_id).all()
    quizid = []
    #for subject in subjects:
    #    if subject.name in subjectsdict.keys():
    #        continue
    #    subjectsdict[subject.name] = 0
    #scores  =  Scores.query.all()
    for score in scores:
        quiz_id = score.quiz_id
        if quiz_id not in quizid:
            quizid.append(quiz_id)
            chapter_id  = (Quiz.query.filter_by(id =  quiz_id).first()).chapter_id
            subject_id = (Chapter.query.filter_by(id = chapter_id).first()).subject_id
            subjectname = (Subject.query.filter_by(id = subject_id).first()).name
            if subjectname not in subjectsdict:
                subjectsdict[subjectname] = 0
            
            subjectsdict[subjectname] += 1
        else:
            continue    
    labels = list(subjectsdict.keys())
    no_of_quizzes_attempted = list(subjectsdict.values())
    plt.bar(labels, no_of_quizzes_attempted, color = "blue")
    plt.title("top scores by subject")
    plt.xlabel("subjects")
    plt.ylabel("subject_wise_quiz_attempted")
    plt.savefig("static/chart_user.png")
    return render_template("summary_user.html")
        
