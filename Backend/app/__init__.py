from flask import Flask
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

    # Registrar blueprints
    app.register_blueprint(main)

    return app