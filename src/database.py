from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(80), unique=True, nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    created_at =db.Column(db.DateTime, default=datetime.now())
    updated_at =db.Column(db.DateTime, default=datetime.now())
    video = db.relationship('Video', backref='user', lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}'"
    
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    creator=db.Column(db.String(80), unique=True, nullable=False)
    duration=db.Column(db.String(5))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f"Post('{self.title}','{self.creator}', '{self.date_posted}')"