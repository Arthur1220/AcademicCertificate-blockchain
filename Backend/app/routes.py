import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from .blockchain import register_institution, verify_institution, register_certificate, get_certificate, transfer_admin
from .storage import save_file, allowed_file
from .models import Certificate
from .extensions import db  # Atualizado aqui
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/register_institution', methods=['POST'])
def register_institution_route():
    """
    Endpoint para registrar uma nova instituição.
    """
    data = request.get_json()
    name = data.get('name')
    cnpj = data.get('cnpj')
    responsible = data.get('responsible')

    try:
        receipt = register_institution(name, cnpj, responsible)
        return jsonify({
            'status': 'success',
            'transaction_hash': receipt.transactionHash.hex()
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@main.route('/verify_institution', methods=['POST'])
def verify_institution_route():
    """
    Endpoint para verificar uma instituição (apenas admin).
    """
    data = request.get_json()
    institution_address = data.get('institution_address')

    try:
        receipt = verify_institution(institution_address)
        return jsonify({
            'status': 'success',
            'transaction_hash': receipt.transactionHash.hex()
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@main.route('/register_certificate', methods=['POST'])
def register_certificate_route():
    """
    Endpoint para registrar um novo certificado.
    Espera-se que o corpo da requisição contenha o arquivo e os dados do certificado.
    """
    certificate_hash = request.form.get('certificate_hash')
    student_name = request.form.get('student_name')
    issue_date = request.form.get('issue_date')  # Formato timestamp
    institution_address = request.form.get('institution_address')

    file = request.files.get('file')

    if not all([certificate_hash, student_name, issue_date, institution_address, file]):
        return jsonify({'status': 'error', 'message': 'Dados incompletos.'}), 400

    if not allowed_file(file.filename):
        return jsonify({'status': 'error', 'message': 'Tipo de arquivo não permitido.'}), 400

    try:
        # Salvar o arquivo
        filepath = save_file(file, certificate_hash)

        # Registrar o certificado na blockchain
        receipt = register_certificate(
            certificate_hash,
            student_name,
            int(issue_date),
            institution_address
        )

        # Adicionar ao banco de dados
        certificate = Certificate(
            certificate_hash=certificate_hash,
            student_name=student_name,
            issue_date=datetime.fromtimestamp(int(issue_date)),
            institution_address=institution_address,
            file_path=filepath
        )
        db.session.add(certificate)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'transaction_hash': receipt.transactionHash.hex(),
            'file_path': filepath
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@main.route('/get_certificate/<certificate_hash>', methods=['GET'])
def get_certificate_route(certificate_hash):
    """
    Endpoint para consultar os detalhes de um certificado.
    """
    try:
        # Obter detalhes da blockchain
        cert_data = get_certificate(certificate_hash)

        # Obter detalhes do banco de dados
        certificate = Certificate.query.filter_by(certificate_hash=certificate_hash).first()
        if not certificate:
            return jsonify({'status': 'error', 'message': 'Certificado não encontrado no banco de dados.'}), 404

        return jsonify({
            'status': 'success',
            'certificate': {
                'student_name': cert_data['studentName'],
                'issue_date': cert_data['issueDate'],
                'institution_address': cert_data['institutionAddress'],
                'file_path': certificate.file_path
            }
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@main.route('/transfer_admin', methods=['POST'])
def transfer_admin_route():
    """
    Endpoint para transferir a função de administrador.
    """
    data = request.get_json()
    new_admin_address = data.get('new_admin_address')

    try:
        receipt = transfer_admin(new_admin_address)
        return jsonify({
            'status': 'success',
            'transaction_hash': receipt.transactionHash.hex()
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
