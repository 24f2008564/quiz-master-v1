from flask import Flask, render_template, redirect, request, url_for,flash
from flask import current_app as app
from .models import *
from datetime import datetime

admin = {
    "username": "24f2008564@ds.study.iitm.ac.in",
    "password": "kshitijiitmadras",

}

@app.route("/", methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        ext_user = User.query.filter_by(username = uname, password = pwd).first()
        
        if ext_user and ext_user.is_admin:
            subjects = Subject.query.all()
            #chapters = Chapter.query.all()
            return render_template("admin_dashbord.html", subjects = subjects)
        elif ext_user:
            return render_template("user_dashboard.html")
        else:
            return render_template("login.html", msg = "Invalid user credentials")
    
    return render_template("login.html", msg="")
    #flash("user not registered")

@app.route("/register", methods = ['GET','POST'])
def register():
    
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form['Password']
        fullname  = request.form['Fullname']   
        qualification = request.form['Qualification']
        dob = request.form['DOB']
        dob_obj = datetime.strptime(dob, '%Y-%m-%d').date()
        if not User.query.filter_by(username = username).first():
            new_user = User(username = username, password = password, fullname = fullname, qualification = qualification, DOB=dob_obj)
            
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            flash("user already exist")
            return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template('register.html')

@app.route("/admin")
def admin():
    subjects = Subject.query.all()
    return render_template("admin_dashbord.html", subjects = subjects)  
      
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
        
    return render_template("addsubject.html")
#   return redirect("/Addsubject")
#return render_template("admin_dashbord.html")    
                 
    #return render_template("addsubject.html")
            

#@app.route("/")

@app.route("/Addchapter/<int:subjectid>/", methods = ['GET','POST'])
def addchapter(subjectid):
    if request.method == 'POST':
        name = request.form['chaptername']
        description = request.form['Description']

        subject = Subject.query.filter_by(id = subjectid).first()
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

@app.route("/Addquiz/<int:chapter_id>/", methods = ['GET','POST'])
def addquiz(chapter_id):
    if request.method == 'GET':
        chapter = Chapter.query.filter_by(id = chapter_id).first()
        if chapter:
            return render_template("addquiz.html", chapter = chapter)
        else:
            return redirect(url_for("/addchapter"))
    
    elif request.method == 'POST':    
        date = request.form['date']
        duration = request.form['duration']
        chapter = Chapter.query.filter_by(id = chapter_id).first()
        new_quiz = Quiz(date_of_quiz  = date, time_duration = duration, chapter_id = chapter.id)
        db.session.add(new_quiz)
        db.session.commit()
        return  redirect(url_for(""))
        
