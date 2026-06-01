from app import db
from app.models.perdido_model import PerdidoModel

class PerdidoService:
    @staticmethod
    def listar_todos():
        return PerdidoModel.query.all()

    @staticmethod
    def obter_por_id(perdido_id):
        return PerdidoModel.query.get(perdido_id)

    @staticmethod
    def criar_perdido(nome, descricao):
        novo_perdido = PerdidoModel(
            nome=nome,
            descricao=descricao
        )
        db.session.add(novo_perdido)
        db.session.commit()
        return novo_perdido