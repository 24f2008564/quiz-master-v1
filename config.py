import os
from dotenv import load_dotenv
from app import app
load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')