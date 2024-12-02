from .extensions import db

class Certificate(db.Model):
    """
    Modelo que representa um certificado armazenado no backend.
    """
    id = db.Column(db.Integer, primary_key=True)
    certificate_hash = db.Column(db.String(66), unique=True, nullable=False)  # 0x + 64 caracteres
    student_name = db.Column(db.String(255), nullable=False)
    issue_date = db.Column(db.DateTime, nullable=False)
    institution_address = db.Column(db.String(42), nullable=False)  # Endereço Ethereum
    file_path = db.Column(db.String(255), nullable=False)  # Caminho para o arquivo armazenado

    def __repr__(self):
        return f"<Certificate {self.certificate_hash} - {self.student_name}>"
