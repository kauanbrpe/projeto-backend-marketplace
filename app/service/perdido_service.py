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

    @staticmethod
    def atualizar_perdido(perdido_id, dados):
        perdido = PerdidoRepository.find_by_id(perdido_id)
        if not perdido:
            raise ValueError("Erro: Perdido não encontrado!")

        if 'nome' in dados:
            perdido.nome = dados['nome']
        if 'descricao' in dados:
            perdido.descricao = dados['descricao']

        return PerdidoRepository.update(perdido)

    @staticmethod
    def deletar_perdido(perdido_id):
        perdido = PerdidoRepository.find_by_id(perdido_id)
        if not perdido:
            raise ValueError("Erro: Perdido não encontrado!")

        PerdidoRepository.delete(perdido)
        return True
