from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('key')
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS=False
db = SQLAlchemy(app)


  