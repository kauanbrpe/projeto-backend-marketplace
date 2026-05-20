from app import db

class PerdidoModel(db.Model):
    __tablename__ = 'perdidos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao
        }
