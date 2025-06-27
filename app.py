# app.py

import urllib.parse
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from models import db, User # Solo necesitamos el modelo User
from controllers import main_bp, auth_bp, mantenedores_bp, mantenedores_usernames_bp # ¡Importa el nuevo Blueprint!


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Por favor, inicia sesión para acceder a esta página."
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):
        """Callback requerido por Flask-Login para cargar un usuario."""
        return User.query.get(int(user_id))

    # Registrar los Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(mantenedores_bp)
    app.register_blueprint(mantenedores_usernames_bp) # ¡REGISTRA EL NUEVO BLUEPRINT!

    return app


if __name__ == '__main__':
    app = create_app()

    # Creación de tablas de la base de datos (solo una vez)
    with app.app_context():
        db.create_all() # Esto creará la tabla 'users' si no existe
        print("Tablas de la base de datos creadas (si no existían).")

    app.run(debug=True)