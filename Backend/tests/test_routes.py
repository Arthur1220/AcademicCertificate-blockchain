# backend/tests/test_routes.py

import os
import tempfile
import pytest
from app.extensions import db
from app.models import Certificate
from unittest.mock import patch, Mock
from datetime import datetime

def test_register_institution(test_client):
    with patch('app.routes.register_institution') as mock_register:
        # Simula um objeto de recibo com o atributo transactionHash
        mock_receipt = Mock()
        mock_receipt.transactionHash = b'0xmockedtransactionhash'
        mock_register.return_value = mock_receipt

        response = test_client.post('/register_institution', json={
            'name': 'Instituição XYZ',
            'cnpj': '12.345.678/0001-90',
            'responsible': 'Prof. João'
        })

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert 'transaction_hash' in response.json

def test_register_certificate(test_client):
    with patch('app.routes.register_certificate') as mock_register_cert:
        # Simula um objeto de recibo com o atributo transactionHash
        mock_receipt = Mock()
        mock_receipt.transactionHash = b'0xmockedtransactionhash'
        mock_register_cert.return_value = mock_receipt

        data = {
            'certificate_hash': '0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
            'student_name': 'Maria Silva',
            'issue_date': '1700000000',
            'institution_address': '0xInstituicaoEndereco'
        }

        # Cria um arquivo temporário para upload
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            tmp_file.write(b'Teste de certificado')
            tmp_file.seek(0)
            file_tuple = (tmp_file, 'certificado.pdf')
            data['file'] = file_tuple

            response = test_client.post(
                '/register_certificate',
                data=data,
                content_type='multipart/form-data'
            )

        # Remove o arquivo temporário após o teste
        os.unlink(tmp_file.name)

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert 'transaction_hash' in response.json
        assert 'file_path' in response.json

def test_get_certificate(test_client):
    with patch('app.routes.get_certificate') as mock_get_cert:
        mock_get_cert.return_value = {
            'studentName': 'Maria Silva',
            'issueDate': 1700000000,
            'institutionAddress': '0xInstituicaoEndereco'
        }

        # Adicionar certificado ao banco de dados
        cert = Certificate(
            certificate_hash='0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
            student_name='Maria Silva',
            issue_date=datetime.fromtimestamp(1700000000),
            institution_address='0xInstituicaoEndereco',
            file_path='./test_storage/0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890.pdf'
        )
        db.session.add(cert)
        db.session.commit()

        response = test_client.get('/get_certificate/0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890')

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['certificate']['student_name'] == 'Maria Silva'
        assert response.json['certificate']['institution_address'] == '0xInstituicaoEndereco'
        assert response.json['certificate']['file_path'] == cert.file_path

def test_verify_institution(test_client):
    with patch('app.routes.verify_institution') as mock_verify:
        # Simula um objeto de recibo com o atributo transactionHash
        mock_receipt = Mock()
        mock_receipt.transactionHash = b'0xmockedtransactionhash'
        mock_verify.return_value = mock_receipt

        response = test_client.post('/verify_institution', json={
            'institution_address': '0xInstituicaoEndereco'
        })

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert 'transaction_hash' in response.json

def test_transfer_admin(test_client):
    with patch('app.routes.transfer_admin') as mock_transfer:
        # Simula um objeto de recibo com o atributo transactionHash
        mock_receipt = Mock()
        mock_receipt.transactionHash = b'0xmockedtransactionhash'
        mock_transfer.return_value = mock_receipt

        response = test_client.post('/transfer_admin', json={
            'new_admin_address': '0xNovoAdminEndereco'
        })

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert 'transaction_hash' in response.json
