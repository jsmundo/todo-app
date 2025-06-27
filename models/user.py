import secrets
from datetime import datetime,timedelta
from models import db
from models.Task import Task

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)
    reset_token = db.Column(db.String(255), nullable=True)
    reset_token_expires = db.Column(db.DateTime, nullable=True)



    def __repr__(self):
        return f'<User {self.username}>'