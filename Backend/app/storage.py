import os
from werkzeug.utils import secure_filename
from flask import current_app

# Definir extensões permitidas
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    """Verifica se a extensão do arquivo é permitida."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file, certificate_hash):
    """
    Salva o arquivo no diretório de armazenamento com o nome baseado no hash do certificado.
    
    :param file: Arquivo enviado pelo usuário
    :param certificate_hash: Hash do certificado na blockchain
    :return: Caminho do arquivo salvo
    """
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Extrair a extensão do arquivo
        ext = filename.rsplit('.', 1)[1].lower()
        # Nomear o arquivo com o hash do certificado
        new_filename = f"{certificate_hash}.{ext}"
        filepath = os.path.join(current_app.config['STORAGE_PATH'], new_filename)
        file.save(filepath)
        return filepath
    else:
        raise ValueError("Arquivo não permitido.")