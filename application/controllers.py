from flask import Flask, render_template, redirect
from flask import current_app as app
from .models import *
@app.route("/")
def login():
    return render_template("login.html")
