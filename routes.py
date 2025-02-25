from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import create_access_token
from flask_babel import gettext as _
from app import app
from models import db
from models.user import User

@app.route('/register', methods=['POST', 'GET'])  
def register():
    print("✅ Recibida petición en /register")

    if request.method == 'GET':
        return jsonify({'message': 'Register endpoint is working'}), 200

    data = request.get_json()
    print("📌 Datos recibidos:", data)

    if not data:
        return jsonify({'error': 'No JSON received'}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Missing data'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    hashed_password = generate_password_hash(password)
    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    print("✅ Usuario registrado")
    
   
    return jsonify({'message': 'Test register working'}), 200  # 🔹 Esto asegura una respuesta válida

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': _('Missing data')}), 400  # 📌 Falta username o password

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'error': _('User not found')}), 404  # 📌 Usuario no encontrado

    if not check_password_hash(user.password, password):
        return jsonify({'error': _('Invalid credentials')}), 401  # 📌 Contraseña incorrecta
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        "access_token": access_token,
        "message": _("Login successful"),
        "user_id": user.id,  
        "email": user.email
    }), 200


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify({
        "message": "You have accssed a protected route",
        "user_id": current_user_id
    }), 200
