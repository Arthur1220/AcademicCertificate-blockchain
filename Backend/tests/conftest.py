import os
import pytest
from app import create_app
from app.extensions import db

@pytest.fixture(scope='function')  # Alterado de 'module' para 'function'
def test_client():
    # Configurar a aplicação para teste
    flask_app = create_app()
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.config['STORAGE_PATH'] = './test_storage'

    # Criar diretório de armazenamento de teste
    if not os.path.exists(flask_app.config['STORAGE_PATH']):
        os.makedirs(flask_app.config['STORAGE_PATH'])

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()
            yield testing_client
            db.session.remove()
            db.drop_all()
