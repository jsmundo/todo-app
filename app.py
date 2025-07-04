from flask import Flask
from flask.cli import with_appcontext
import click
from flask import Flask, request
from flask_mail import Mail
from flask_cors import CORS
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import Config
from models import Task, db


app = Flask(__name__)
app.config.from_object(Config)

mail = Mail(app)
CORS(app, origins= "http://localhost:3000")

db.init_app(app)
migrate = Migrate(app, db)

jwt = JWTManager(app)

# Configurar la selección de idioma en Flask-Babel 4.0.0
def get_locale():
    return request.accept_languages.best_match(['en', 'es'])

babel = Babel(locale_selector=get_locale) 
babel.init_app(app)

# Importa las rutas después de definir `app`
from routes import *

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


def home():
    return "To-Do App Backend Running!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
