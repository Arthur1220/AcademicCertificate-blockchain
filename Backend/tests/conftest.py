# tests/conftest.py

import os
import pytest
from app import create_app
from app.extensions import db

@pytest.fixture(scope='function')  # Usando 'function' para isolamento entre testes
def test_client():
    # Definir configurações de teste
    test_config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'STORAGE_PATH': './test_storage'
    }

    # Criar a aplicação com a configuração de teste
    flask_app = create_app(config_object=test_config)

    # Criar diretório de armazenamento de teste
    if not os.path.exists(flask_app.config['STORAGE_PATH']):
        os.makedirs(flask_app.config['STORAGE_PATH'])

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()
            yield testing_client
            db.session.remove()
            db.drop_all()

    # Limpar o diretório de armazenamento de teste após os testes
    if os.path.exists(flask_app.config['STORAGE_PATH']):
        for root, dirs, files in os.walk(flask_app.config['STORAGE_PATH'], topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(flask_app.config['STORAGE_PATH'])
