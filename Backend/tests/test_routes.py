# tests/test.py

import os
import tempfile
import pytest
from app.extensions import db
from app.models import Certificate
from datetime import datetime

def test_register_certificate(test_client):
    data = {
        'certificate_code': 'CERT123456',
        'student_name': 'Maria Silva',
        'issue_date': '1700000000',  # Timestamp
        'signature': '0xSignature',
        'user_address': '0xUsuarioEndereco',
        'transaction_hash': '0xTransactionHash'
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
    assert 'file_path' in response.json

    # Verificar no banco de dados
    cert = Certificate.query.filter_by(certificate_code=data['certificate_code']).first()
    assert cert is not None
    assert cert.certificate_code == data['certificate_code']
    assert cert.student_name == data['student_name']
    assert cert.issue_date == datetime.fromtimestamp(int(data['issue_date']))
    assert cert.user_address == data['user_address']
    assert cert.transaction_hash == data['transaction_hash']
    assert cert.file_path == response.json['file_path']


def test_get_certificate_by_code(test_client):
    # Adicionar certificado ao banco de dados
    cert = Certificate(
        certificate_code='CERT123456',
        student_name='Maria Silva',
        issue_date=datetime.fromtimestamp(1700000000),
        user_address='0xUsuarioEndereco',
        transaction_hash='0xTransactionHash',
        file_path='./test_storage/CERT123456.pdf'
    )
    db.session.add(cert)
    db.session.commit()

    response = test_client.get('/get_certificate?certificate_code=CERT123456')

    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['certificate']['student_name'] == 'Maria Silva'
    assert response.json['certificate']['codigo_certificado'] == 'CERT123456'
    assert response.json['certificate']['issue_date'] == cert.issue_date.timestamp()
    assert response.json['certificate']['user_address'] == '0xUsuarioEndereco'
    assert response.json['certificate']['transaction_hash'] == '0xTransactionHash'
    assert response.json['certificate']['file_path'] == cert.file_path


def test_get_certificates_by_student_name(test_client):
    # Adicionar certificados ao banco de dados
    cert1 = Certificate(
        certificate_code='CERT123457',
        student_name='Maria Silva',
        issue_date=datetime.fromtimestamp(1700000000),
        user_address='0xUsuarioEndereco',
        transaction_hash='0xTransactionHash1',
        file_path='./test_storage/CERT123457.pdf'
    )
    cert2 = Certificate(
        certificate_code='CERT123458',
        student_name='Maria Silva',
        issue_date=datetime.fromtimestamp(1700000001),
        user_address='0xUsuarioEndereco',
        transaction_hash='0xTransactionHash2',
        file_path='./test_storage/CERT123458.pdf'
    )
    db.session.add(cert1)
    db.session.add(cert2)
    db.session.commit()

    response = test_client.get('/get_certificate?student_name=Maria%20Silva')

    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert len(response.json['certificates']) == 2

    # Verificar o primeiro certificado
    assert response.json['certificates'][0]['student_name'] == 'Maria Silva'
    assert response.json['certificates'][0]['codigo_certificado'] == 'CERT123457'
    assert response.json['certificates'][0]['issue_date'] == cert1.issue_date.timestamp()
    assert response.json['certificates'][0]['user_address'] == '0xUsuarioEndereco'
    assert response.json['certificates'][0]['transaction_hash'] == '0xTransactionHash1'
    assert response.json['certificates'][0]['file_path'] == cert1.file_path

    # Verificar o segundo certificado
    assert response.json['certificates'][1]['student_name'] == 'Maria Silva'
    assert response.json['certificates'][1]['codigo_certificado'] == 'CERT123458'
    assert response.json['certificates'][1]['issue_date'] == cert2.issue_date.timestamp()
    assert response.json['certificates'][1]['user_address'] == '0xUsuarioEndereco'
    assert response.json['certificates'][1]['transaction_hash'] == '0xTransactionHash2'
    assert response.json['certificates'][1]['file_path'] == cert2.file_path
