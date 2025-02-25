from flask import Flask, render_template, redirect, request, url_for,flash
from flask import current_app as app
from .models import *
from datetime import datetime


@app.route("/", methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        ext_user = User.query.filter_by(username = uname, password = pwd).first()
        if ext_user and ext_user.is_admin:
            return render_template("admin_dashbord.html")
        else:
            return render_template("user_dashboard.html")
        
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
        
    