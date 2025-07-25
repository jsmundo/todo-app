



from flask import Flask, request
from flask.cli import with_appcontext
import click

# Blueprints
from routes_new.learn import bp as learn_bp

# Extensiones
from flask_mail import Mail
from flask_cors import CORS
from flask_babel import Babel
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flasgger import Swagger

# Config y modelos
from config import Config
from models import db, Task

app = Flask(__name__)
app.config.from_object(Config)

# --- Extensiones ---
mail = Mail(app)
CORS(app, origins=[
    "http://localhost:3000",
    "http://localhost:5173",
    "https://tu-frontend-en-produccion.com"
])

db.init_app(app)
migrate = Migrate(app, db)

jwt = JWTManager(app)

babel = Babel(app, locale_selector=lambda: request.accept_languages.best_match(['en', 'es']))

swagger_template = {  "swagger": "2.0",
    "info": {
        "title": "Mi API de Tareas",
        "description": "Documentación Swagger para la API de tareas",
        "version": "1.0"
    },
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Token JWT. Usa el prefijo 'Bearer'. Ej: Bearer eyJ..."
        }
    },
    "security": [
        {
            "BearerAuth": []
        }
    ] }  # (dejas tu template igual)
swagger = Swagger(app, template=swagger_template)

# --- Blueprints ---
app.register_blueprint(learn_bp)

# --- Rutas existentes ---
from routes import *

# --- Comandos CLI personalizados ---  (los de limpiar tareas/usuarios …)
# ... tu código CLI sin cambios ...
@app.cli.command("limpiar-tareas-huerfanas")
@with_appcontext
def limpiar_tareas_huerfanas():
    tareas_huerfanas = Task.query.filter(Task.user_id == None).all()
    if not tareas_huerfanas:
        click.echo("✅ No hay tareas huérfanas que eliminar.")
        return

    click.echo(f"⚠️ Se encontraron {len(tareas_huerfanas)} tareas huérfanas.")
    confirmar = input("¿Estás seguro de que querés eliminarlas? (s/n): ")
    if confirmar.lower() == "s":
        for tarea in tareas_huerfanas:
            db.session.delete(tarea)
        db.session.commit()
        click.echo("🗑 Tareas huérfanas eliminadas con éxito.")
    else:
        click.echo("❌ Operación cancelada.")

@app.cli.command("eliminar-usuarios-de-prueba")
@with_appcontext
def eliminar_usuarios_de_prueba():
    from models.user import User
    usuarios = User.query.filter(
        User.email.like("%@test.com") | User.username.like("prueba%")
    ).all()

    if not usuarios:
        click.echo("✅ No se encontraron usuarios de prueba.")
        return

    click.echo(f"⚠️ Se encontraron {len(usuarios)} usuarios de prueba.")
    confirmar = input("¿Querés eliminarlos? (s/n): ")
    if confirmar.lower() == "s":
        for user in usuarios:
            db.session.delete(user)
        db.session.commit()
        click.echo("🗑 Usuarios de prueba eliminados con éxito.")
    else:
        click.echo("❌ Operación cancelada.")
        
@app.cli.command("borrar-todo")
@with_appcontext
def borrar_todo():
    from models import Task
    from models.user import User

    confirm = input("⚠️ ¿Seguro que querés borrar TODOS los usuarios y tareas? (s/n): ")
    if confirm.lower() != "s":
        print("❌ Operación cancelada.")
        return

    Task.query.delete()
    User.query.delete()
    db.session.commit()
    print("✅ Todos los usuarios y tareas han sido eliminados.")

if __name__ == "__main__":
    app.run(debug=True)

