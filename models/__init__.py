from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


from models.user import User
from models.task import Task