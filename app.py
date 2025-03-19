from flask import Flask
from application.database import db
from application.api_controllers import *
#from init import app




   
#import config
#from models import db
#import routes
#with app.app_context():
#    db.create_all()
#import models
#import routes
#db = SQLAlchemy(app)
def create_app():
    app = Flask(__name__)
    app.debug =True
    app.config['SECRET_KEY'] = "8209779608"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///quize_master.sqlite3"
    db.init_app(app)
    api.init_app(app)
    app.app_context().push()
   
    return app

app = create_app()

from application.controllers import *

db.create_all()

#@app.route("/")
#def home():
#    return "LaLA"





if __name__ == '__main__':
    
    app.run(debug=True)