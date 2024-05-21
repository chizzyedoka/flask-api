from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

os.environ.get(app.config['SECRET_KEY'])
os.environ.get(app.config['SQLALCHEMY_DATABASE_URI'])
db = SQLAlchemy(app)

