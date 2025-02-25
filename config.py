import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave_secreta')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tasks.db'
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')
    SQLALCHEMY_TRACK_MODIFICATIONS = False