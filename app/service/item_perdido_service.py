from app.models.item_perdido_model import ItemPerdidoModel
from app.repository import ItemPerdidoRepository

class ItemPerdidoService:
    @staticmethod
    def listar_todos():
        return ItemPerdidoRepository.listar_itens()

    @staticmethod
    def listar_por_id(item_id):
        return ItemPerdidoRepository.buscar_por_id(item_id)

    @staticmethod
    def listar_por_usuario_id(usuario_id):
        return ItemPerdidoRepository.buscar_por_id(usuario_id)

    @staticmethod
    def criar_item_perdido(dados):
        novo_item = ItemPerdidoModel(
            nome_item=dados['nome_item'],
            descricao=dados['descricao'],
            local_perdido=dados['local_perdido'],
            data_perdido=dados['data_perdido'],
            perdido_id=dados['perdido_id'],
            usuario_id=dados['usuario_id']
        )

        return ItemPerdidoRepository.criar_item(novo_item)