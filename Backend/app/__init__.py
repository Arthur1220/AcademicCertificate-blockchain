from flask import Flask
from flask_cors import CORS
from .extensions import db, migrate
from .routes import main
import os

def create_app():
    app = Flask(__name__)

    # Configurações
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['STORAGE_PATH'] = os.getenv('STORAGE_PATH')

    # Inicializar extensões
    db.init_app(app)
    migrate.init_app(app, db)

    # Configurar CORS para permitir todas as conexões
    CORS(app)  # Permite todas as origens por padrão

    # Registrar blueprints
    app.register_blueprint(main)

    return app