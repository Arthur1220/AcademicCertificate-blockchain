import os
import tempfile
import pytest
from app.extensions import db
from app.models import Certificate
from unittest.mock import patch, Mock
from datetime import datetime

def test_register_certificate(test_client):
    with patch('app.routes.register_certificate') as mock_register_cert:
        # Simula um objeto de recibo com o atributo transactionHash e o endereço do emissor
        mock_receipt = Mock()
        mock_receipt.transactionHash = b'0xmockedtransactionhash'
        mock_register_cert.return_value = (mock_receipt, '0xEmissorEndereco')

        data = {
            'certificate_hash': '0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
            'student_name': 'Maria Silva',
            'issue_date': '1700000000',
            'issuer_private_key': '0xPrivateKey'
        }

        # Cria um arquivo temporário para upload
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            tmp_file.write(b'Teste de certificado')
            tmp_file.seek(0)
            data['file'] = (tmp_file, 'certificado.pdf')

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

def test_get_certificate_by_hash(test_client):
    with patch('app.routes.get_certificate') as mock_get_cert:
        mock_get_cert.return_value = {
            'studentName': 'Maria Silva',
            'issueDate': 1700000000,
            'issuerAddress': '0xEmissorEndereco'
        }

        # Adicionar certificado ao banco de dados
        cert = Certificate(
            certificate_hash='0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890',
            student_name='Maria Silva',
            issue_date=datetime.fromtimestamp(1700000000),
            issuer_address='0xEmissorEndereco',
            file_path='./test_storage/0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890.pdf'
        )
        db.session.add(cert)
        db.session.commit()

        response = test_client.get('/get_certificate?certificate_hash=0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890')

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert response.json['certificate']['student_name'] == 'Maria Silva'
        assert response.json['certificate']['issuer_address'] == '0xEmissorEndereco'
        assert response.json['certificate']['file_path'] == cert.file_path

def test_get_certificates_by_student_name(test_client):
    with patch('app.routes.get_certificate') as mock_get_cert:
        # Mock para retornar dados para cada hash de certificado
        def mock_get_certificate_side_effect(certificate_hash):
            return {
                'studentName': 'Maria Silva',
                'issueDate': 1700000000,
                'issuerAddress': '0xEmissorEndereco'
            }
        mock_get_cert.side_effect = mock_get_certificate_side_effect

        # Adicionar certificados ao banco de dados
        cert1 = Certificate(
            certificate_hash='0xhash1',
            student_name='Maria Silva',
            issue_date=datetime.fromtimestamp(1700000000),
            issuer_address='0xEmissorEndereco',
            file_path='./test_storage/0xhash1.pdf'
        )
        cert2 = Certificate(
            certificate_hash='0xhash2',
            student_name='Maria Silva',
            issue_date=datetime.fromtimestamp(1700000001),
            issuer_address='0xEmissorEndereco',
            file_path='./test_storage/0xhash2.pdf'
        )
        db.session.add(cert1)
        db.session.add(cert2)
        db.session.commit()

        response = test_client.get('/get_certificate?student_name=Maria%20Silva')

        assert response.status_code == 200
        assert response.json['status'] == 'success'
        assert len(response.json['certificates']) == 2

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