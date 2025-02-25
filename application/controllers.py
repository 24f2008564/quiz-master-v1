from flask import Flask, render_template, redirect, request, url_for,flash
from flask import current_app as app
from .models import *
from datetime import datetime


@app.route("/")
def login():
    return render_template("login.html")

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
        
    