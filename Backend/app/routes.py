import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from .blockchain import register_certificate, get_certificate, transfer_admin
from .storage import save_file, allowed_file
from .models import Certificate
from .extensions import db
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/register_certificate', methods=['POST'])
def register_certificate_route():
    """
    Endpoint para registrar um novo certificado.
    Espera-se que o corpo da requisição contenha o arquivo e os dados do certificado.
    """
    certificate_hash = request.form.get('certificate_hash')
    student_name = request.form.get('student_name')
    issue_date = request.form.get('issue_date')  # Formato timestamp
    issuer_private_key = request.form.get('issuer_private_key')

    file = request.files.get('file')

    if not all([certificate_hash, student_name, issue_date, issuer_private_key, file]):
        return jsonify({'status': 'error', 'message': 'Dados incompletos.'}), 400

    if not allowed_file(file.filename):
        return jsonify({'status': 'error', 'message': 'Tipo de arquivo não permitido.'}), 400

    try:
        # Salvar o arquivo
        filepath = save_file(file, certificate_hash)

        # Registrar o certificado na blockchain
        receipt, issuer_address = register_certificate(
            certificate_hash,
            student_name,
            int(issue_date),
            issuer_private_key
        )

        # Adicionar ao banco de dados
        certificate = Certificate(
            certificate_hash=certificate_hash,
            student_name=student_name,
            issue_date=datetime.fromtimestamp(int(issue_date)),
            issuer_address=issuer_address,
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

@main.route('/get_certificate', methods=['GET'])
def get_certificate_route():
    """
    Endpoint para consultar os detalhes de um certificado.
    Pode pesquisar por 'certificate_hash' ou 'student_name' como parâmetros de consulta.
    """
    certificate_hash = request.args.get('certificate_hash')
    student_name = request.args.get('student_name')

    if certificate_hash:
        # Procurar pelo hash do certificado
        try:
            # Obter detalhes da blockchain
            cert_data = get_certificate(certificate_hash)
            if not cert_data:
                return jsonify({'status': 'error', 'message': 'Certificado não encontrado na blockchain.'}), 404

            # Obter detalhes do banco de dados
            certificate = Certificate.query.filter_by(certificate_hash=certificate_hash).first()
            if not certificate:
                return jsonify({'status': 'error', 'message': 'Certificado não encontrado no banco de dados.'}), 404

            return jsonify({
                'status': 'success',
                'certificate': {
                    'student_name': cert_data['studentName'],
                    'issue_date': cert_data['issueDate'],
                    'issuer_address': cert_data['issuerAddress'],
                    'file_path': certificate.file_path
                }
            }), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 400
    elif student_name:
        # Procurar por nome do estudante
        certificates = Certificate.query.filter_by(student_name=student_name).all()
        if not certificates:
            return jsonify({'status': 'error', 'message': 'Nenhum certificado encontrado para este nome.'}), 404

        # Obter detalhes de cada certificado
        cert_list = []
        for cert in certificates:
            cert_data = get_certificate(cert.certificate_hash)
            if cert_data:
                cert_info = {
                    'student_name': cert_data['studentName'],
                    'issue_date': cert_data['issueDate'],
                    'issuer_address': cert_data['issuerAddress'],
                    'file_path': cert.file_path
                }
                cert_list.append(cert_info)

        return jsonify({
            'status': 'success',
            'certificates': cert_list
        }), 200
    else:
        return jsonify({'status': 'error', 'message': 'Parâmetros de busca inválidos. Informe "certificate_hash" ou "student_name".'}), 400

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