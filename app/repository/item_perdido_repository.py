from app.models.item_perdido_model import ItemPerdidoModel
from app import db

class ItemPerdidoRepository:

    @staticmethod
    def criar_item(data):
        novo_item = ItemPerdidoModel(
            nome_item=data['nome_item'],
            descricao=data['descricao'],
            local_perdido=data['local_perdido'],
            data_perdido=data['data_perdido'],
            perdido_id=data['perdido_id'],
            usuario_id=data['usuario_id']
        )
        db.session.add(novo_item)
        db.session.commit()
        return novo_item

    @staticmethod
    def listar_itens():
        return ItemPerdidoModel.query.all()

    @staticmethod
    def buscar_por_id(item_id):
        return ItemPerdidoModel.query.get(item_id)

    @staticmethod
    def atualizar_item(item, data):
        item.nome_item = data.get('nome_item', item.nome_item)
        item.descricao = data.get('descricao', item.descricao)
        item.local_perdido = data.get('local_perdido', item.local_perdido)
        item.data_perdido = data.get('data_perdido', item.data_perdido)
        item.perdido_id = data.get('perdido_id', item.perdido_id)
        item.usuario_id = data.get('usuario_id', item.usuario_id)
        db.session.commit()
        return item

    @staticmethod
    def deletar_item(item):
        db.session.delete(item)
        db.session.commit()
        return True
