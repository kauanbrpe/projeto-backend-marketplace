from app import db
from app.models.item_perdido_model import ItemPerdidoModel

class ItemPerdidoService:
    @staticmethod
    def listar_todos():
        return ItemPerdidoModel.query.all()

    @staticmethod
    def obter_por_id(item_id):
        return ItemPerdidoModel.query.get(item_id)

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
        db.session.add(novo_item)
        db.session.commit()
        return novo_item