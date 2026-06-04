from app.models.perdido_model import PerdidoModel
from app.repository import PerdidoRepository

class PerdidoService:
    @staticmethod
    def listar_todos():
        return PerdidoRepository.find_all()

    @staticmethod
    def listar_por_id(perdido_id):
        return PerdidoRepository.find_by_id(perdido_id)

    @staticmethod
    def criar_perdido(nome, descricao):
        novo_perdido = PerdidoModel(
            nome=nome,
            descricao=descricao
        )

        return PerdidoRepository.save(novo_perdido)