from app import db

class ItemPerdidoModel(db.Model):
    __tablename__ = 'itens_perdidos'

    id = db.Column(db.Integer, primary_key=True)
    nome_item = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    local_perdido = db.Column(db.String(120), nullable=False)
    data_perdido = db.Column(db.String(20), nullable=False)
    perdido_id = db.Column(db.Integer, db.ForeignKey('perdidos.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nome_item": self.nome_item,
            "descricao": self.descricao,
            "local_perdido": self.local_perdido,
            "data_perdido": self.data_perdido,
            "perdido_id": self.perdido_id,
            "usuario_id": self.usuario_id
        }
