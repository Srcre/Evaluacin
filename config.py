# config.py
import os
import urllib.parse

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una_clave_secreta_muy_dificil_de_adivinar'

    # Contraseña de la base de datos (se usa para codificarla)
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'admin' # Tu contraseña de MySQL

    # Codifica la contraseña para la URL de la base de datos
    ENCODED_DB_PASSWORD = urllib.parse.quote_plus(DB_PASSWORD)

    # Configura la cadena de conexión con la contraseña codificada
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://root:{ENCODED_DB_PASSWORD}@localhost:3306/mi_app_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Desactiva el seguimiento de modificaciones de objetos