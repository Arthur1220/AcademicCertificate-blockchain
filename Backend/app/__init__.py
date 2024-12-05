from flask import Flask
from flask_cors import CORS
from .extensions import db, migrate
from .routes import main
import os

def create_app(config_object=None):
    app = Flask(__name__)

    if config_object:
        app.config.from_object(config_object)
    else:
        # Carregar configurações padrão
        app.config.from_object('config.default.Config')  # Caminho completo para a classe Config

    # Inicializar extensões
    db.init_app(app)
    migrate.init_app(app, db)

    # Configurar CORS para permitir todas as conexões
    CORS(app)  # Permite todas as origens por padrão; ajuste conforme necessário

    # Registrar blueprints
    app.register_blueprint(main)

    return app