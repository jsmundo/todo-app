
from models import db
from models.task import Task

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)



    def __repr__(self):
        return f'<User {self.username}>'