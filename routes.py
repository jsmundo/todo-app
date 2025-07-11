from flask import request, jsonify, url_for
import secrets 
from flask_mail import Message
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_babel import gettext as _
from app import app, mail, db
from models import db, Task
from models.user import User
from swagger_docs import register_doc, login_doc, get_tasks_doc, create_task_doc, get_task_doc, update_task_doc, delete_task_doc, mark_task_done_doc
from flasgger import swag_from

#Ruta de registro
@app.route('/register', methods=['POST', 'GET'])
@swag_from(register_doc)
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
    return jsonify({'message': 'Test register working'}), 200  

# Ruta para loguearte
@app.route('/login', methods=['POST'])
@swag_from(login_doc)
def login():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': _('Missing data')}), 400  # 📌 Falta username o password
    email = data.get('email')
    password = data.get('password')

    print("📩 Email recibido:", email)

    user = User.query.filter_by(email=email).first()
    if not user:
        print("❌ Usuario no encontrado en la base de datos")
        return jsonify({'error': _('User not found')}), 404
    print("✅ Usuario encontrado:", user.username, "ID:", user.id)

      # 📌 Usuario no encontrado
    if not check_password_hash(user.password, password):
        print("❌ Contraseña incorrecta para", email)
        auth = request.headers.get("Authorization")
        print("🔐 HEADER Authorization:", auth)

        return jsonify({'error': _('Invalid credentials')}), 401  # 📌 Contraseña incorrecta
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "message": _("Login successful"),
        "user_id": user.id,  
        "email": user.email
          }), 200

@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(accss_token=new_access_token),200


#Ruta obtener tareas del usuario autenticado
@app.route("/tareas", methods=["GET"])
@swag_from(get_tasks_doc)
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    print("🔐 USER_ID del token:", user_id)
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([task.serialize() for task in tasks]), 200

# Ruta para crear nueva tarea
@app.route("/tareas", methods=["POST"])
@swag_from(create_task_doc)
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    if not title or not description:
        return jsonify({"error": "Title y description son requeridos"}),400
    new_task = Task(
        title=title,
        description=description,
        user_id=user_id
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.serialize()),201


#obtener la tarea por su id
@app.route("/tareas/<int:id>", methods=["GET"])
@swag_from(get_task_doc)
@jwt_required()
def get_task(id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=id, user_id=user_id).first()
    if not task:
        return jsonify({"error": "Tarea no encontrada"}), 404
    return jsonify(task.serialize()),200

# Ruta actulizar el titulo y description
@app.route("/tareas/<int:id>", methods=["PUT"])
@swag_from(update_task_doc)
@jwt_required()
def update_task(id):
    user_id = get_jwt_identity()
    data = request.get_json()
    task = Task.query.filter_by(id=id, user_id=user_id).first()
    if not task:
        return jsonify({"error": "Tarea no en controtrda"}), 404
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    db.session.commit()
    return jsonify(task.serialize()), 200

# Ruta para marcar tarea como hecha
@app.route("/tareas/<int:id>/done", methods=["PATCH"])
@swag_from(mark_task_done_doc)
@jwt_required()
def mark_task_done(id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=id, user_id=user_id).first()
    if not task:
        return jsonify({"error": "Tarea no encontrada"}), 400
    task.done = True
    task.completed = datetime.now()
    db.session.commit()
    return jsonify(task.serialize()),200

#Ruta para borrar taraeas
@app.route("/tareas/<int:id>", methods=["DELETE"])
@swag_from(delete_task_doc)
@jwt_required()
def delete_task(id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=id, user_id=user_id).first()
    if not task:
        return jsonify({"error": "Tarea no encontrada"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Tarea eliminada"}),200

#Esto es para proteger mis rutas 
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify({
        "message": "You have accssed a protected route",
        "user_id": current_user_id
    }), 200

#Genero token para la recuperacion del password
@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
     # 📌 Verificar si el correo electrónico existe en la base de datos
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'Email not found'}), 404
    reset_token = secrets.token_urlsafe(32)
    user.reset_token = reset_token
    user.reset_token_expires = datetime.now() + timedelta(minutes=15)
    db.session.commit()
    # 📌 Enviar correo electrónico con el enlace de restablecimiento de contraseña
    reset_link = f"{app.config['FRONTEND_URL']}/reset-password/{reset_token}"
    # 📌 Crear mensaje de correo electrónico
    msg = Message(
        "Recuperación de Contraseña",
        sender=app.config['MAIL_DEFAULT_SENDER'],
        recipients=[email]
    )
    msg.body = f"Hola, usa el siguiente enlace para restablecer tu contraseña:\n {reset_link}"
    try:
        mail.send(msg)
        return jsonify({'message': 'Correo de recuperación enviado.'}), 200
    except Exception as e:
        return jsonify({'error': f'Error enviando correo: {str(e)}'}), 500
    
#Validacion del token 
@app.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    data = request.get_json()
    new_password = data.get("new_password")
    if not new_password:
        return jsonify({"error": "Password is requerido"}),400
    user = User.query.filter_by(reset_token=token).first()
    if not user or user.reset_token_expires <datetime.now():
        return jsonify({"error": "Token invalido o expirado"}),400
    user.password = generate_password_hash(new_password)
    user.reset_token = None
    user.reset_token_expires = None
    db.session.commit()
    return jsonify({"message": "Password reset successful"}),200


   
    




