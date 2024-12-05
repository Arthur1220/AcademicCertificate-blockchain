from .extensions import db

class Certificate(db.Model):
    """
    Modelo que representa um certificado armazenado no backend.
    """
    id = db.Column(db.Integer, primary_key=True)
    certificate_code = db.Column(db.String(255), unique=True, nullable=False)  # Código que fica registrado no próprio certificado
    student_name = db.Column(db.String(255), nullable=False)
    issue_date = db.Column(db.DateTime, nullable=False)
    user_address = db.Column(db.String(42), nullable=False)  # Endereço Ethereum do usuário que emitiu o certificado
    transaction_hash = db.Column(db.String(66), nullable=False)  # Hash da transação que emitiu o certificado
    file_path = db.Column(db.String(255), nullable=False)  # Caminho para o arquivo armazenado

    def __repr__(self):
        return f"<Certificate {self.certificate_code} - {self.student_name} - {self.user_address}>"