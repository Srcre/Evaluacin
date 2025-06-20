# app.py
import urllib.parse
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, User # Importa db y User de models.py
from controllers import main_bp, auth_bp # Importa los Blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # Inicializar Flask-SQLAlchemy
    db.init_app(app)

    # Inicializar Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' # Ruta a la que se redirige si no está logeado
    login_manager.login_message = "Por favor, inicia sesión para acceder a esta página."
    login_manager.login_message_category = "warning"

    # Tu contraseña con caracteres especiales
    my_password = '49^!M&*TC2*g!tb*pR@c!x8@localhost'

    # Codifica la contraseña para URL
    ncoded_password = urllib.parse.quote_plus(my_password)

    # Configura la cadena de conexión con la contraseña codificada
    # Asegúrate de que el host sea 'localhost' o '127.0.0.1' y el nombre de tu base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{ncoded_password}@localhost:3306/nombre_de_tu_base_de_datos'

    # Ejemplo: Imprime la URI para verificarla
    print(f"SQLALCHEMY_DATABASE_URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

    # Tu código de inicialización de db y modelos (db.create_all(), etc.)
    # ...
    @login_manager.user_loader
    def load_user(user_id):
        """Callback requerido por Flask-Login para cargar un usuario."""
        return User.query.get(int(user_id))

    # Registrar los Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app

if __name__ == '__main__':
    app = create_app()

    # Creación de tablas de la base de datos (solo una vez)
    # Se recomienda ejecutar esto en un shell de Python o en un script de migración
    with app.app_context():
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:7@49^!M&*TC2*g!tb*pR@c!x8@localhost/mi_app_db'
        print("Tablas de la base de datos creadas (si no existían).")

    app.run(debug=True) # debug=True para desarrollo, cambiar a False en producción