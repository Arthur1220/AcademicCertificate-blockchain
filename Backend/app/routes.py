import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
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
    print(request.form.get('certificate_code'))
    print(request.files.get('file'))
    certificate_code = request.form.get('certificate_code')
    student_name = request.form.get('student_name')
    issue_date = request.form.get('issue_date')  # Formato timestamp
    user_address = request.form.get('user_address')
    transaction_hash = request.form.get('transaction_hash')

    file = request.files.get('file')

    # Verificar se todos os dados necessários estão presentes
    if not all([certificate_code, student_name, issue_date, user_address, transaction_hash, file]):
        return jsonify({'status': 'error', 'message': 'Dados incompletos.'}), 400

    # Verificar se o arquivo possui uma extensão permitida
    if not allowed_file(file.filename):
        return jsonify({'status': 'error', 'message': 'Tipo de arquivo não permitido.'}), 400

    try:
        # Salvar o arquivo
        filepath = save_file(file, certificate_code)

        # Adicionar ao banco de dados
        certificate = Certificate(
            certificate_code=certificate_code,
            student_name=student_name,
            issue_date=datetime.fromtimestamp(int(issue_date)),
            user_address=user_address,
            transaction_hash=transaction_hash,
            file_path=filepath
        )
        db.session.add(certificate)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'file_path': filepath
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@main.route('/get_certificate', methods=['GET'])
def get_certificate_route():
    """
    Endpoint para consultar os detalhes de um certificado.
    Pode pesquisar por 'certificate_code' ou 'student_name' como parâmetros de consulta.
    """
    certificate_code = request.args.get('certificate_code')
    student_name = request.args.get('student_name')

    if certificate_code:
        # Procurar pelo código do certificado
        try:
            # Buscar no banco de dados
            certificate = Certificate.query.filter_by(certificate_code=certificate_code).first()
            if not certificate:
                return jsonify({'status': 'error', 'message': 'Certificado não encontrado no banco de dados.'}), 404

            return jsonify({
                'status': 'success',
                'certificate': {
                    'student_name': certificate.student_name,
                    'codigo_certificado': certificate.certificate_code,
                    'issue_date': certificate.issue_date.timestamp(),
                    'user_address': certificate.user_address,
                    'transaction_hash': certificate.transaction_hash,
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
            cert_info = {
                'student_name': cert.student_name,
                'codigo_certificado': cert.certificate_code,
                'issue_date': cert.issue_date.timestamp(),
                'user_address': cert.user_address,
                'transaction_hash': cert.transaction_hash,
                'file_path': cert.file_path
            }
            cert_list.append(cert_info)

        return jsonify({
            'status': 'success',
            'certificates': cert_list
        }), 200
    else:
        return jsonify({'status': 'error', 'message': 'Parâmetros de busca inválidos. Informe "certificate_code" ou "student_name".'}), 400
