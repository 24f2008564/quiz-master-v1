from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

import config
import models
import routes
#db = SQLAlchemy(app)
#
#
#class User(db.Model):
#    id = (db.Column



@app.route("/")
def home():
    return "LaLA"





if __name__ == '__main__':
    app.run(debug=True)