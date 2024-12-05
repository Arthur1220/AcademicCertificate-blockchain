# config/default.py

import os

class Config:
    """
    Configurações padrão para a aplicação Flask.
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///certificates.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STORAGE_PATH = os.environ.get('STORAGE_PATH', './storage')