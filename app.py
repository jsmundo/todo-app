from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
jwt = JWTManager(app)

@app.route('/')
def home():
    return "To-Do App Backend Running!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)