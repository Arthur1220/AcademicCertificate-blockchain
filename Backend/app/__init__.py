import os
from flask import Flask

# Carregar configurações do arquivo .env
from dotenv import load_dotenv
load_dotenv()

from .extensions import db, migrate

def create_app():
    app = Flask(__name__)

    # Configurações
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///certificates.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['STORAGE_PATH'] = os.getenv('STORAGE_PATH', './storage')

    # Inicializar extensões
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar blueprints ou rotas
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app