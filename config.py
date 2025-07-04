import os
from dotenv import load_dotenv
from datetime import timedelta


load_dotenv()

class Config:
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'clave_jwt_secreta')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=15)
    JWT_REFRESH_TOKEN_EXPIRES =timedelta(days=30)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tasks.db'
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False').lower() ==  'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME') # 📌 Correo de la cuenta de correo
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD') # 📌 Contraseña de la cuenta de correo
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER' , MAIL_USERNAME)


print("📌 MAIL_SERVER:", Config.MAIL_SERVER)
print("📌 MAIL_PORT:", Config.MAIL_PORT)
print("📌 MAIL_USERNAME:", Config.MAIL_USERNAME)
print("📌 FRONTEND_URL:", Config.FRONTEND_URL)    
