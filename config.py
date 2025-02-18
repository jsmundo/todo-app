import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave_secreta')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tasks.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False