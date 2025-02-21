from flask import Flask, request
from flask_cors import CORS
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, origins= "http://localhost:3000")

db.init_app(app)
jwt = JWTManager(app)

# Configurar la selección de idioma en Flask-Babel 4.0.0
def get_locale():
    return request.accept_languages.best_match(['en', 'es'])

babel = Babel(locale_selector=get_locale)  # Solo esta línea es suficiente
babel.init_app(app)

# Importa las rutas después de definir `app`
from routes import *


def home():
    return "To-Do App Backend Running!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
