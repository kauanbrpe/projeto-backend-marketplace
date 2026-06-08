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
        from app.models.item_perdido_model import ItemPerdidoModel
        return ItemPerdidoModel.query.filter_by(usuario_id=usuario_id).all()

    @staticmethod
    def criar_item_perdido(dados):
        return ItemPerdidoRepository.criar_item(dados)

    @staticmethod
    def atualizar_item_perdido(item_id, dados, current_user):
        item = ItemPerdidoRepository.buscar_por_id(item_id)
        if not item:
            raise ValueError("Erro: Item perdido não encontrado!")

        if item.usuario_id != current_user.id and not current_user.is_admin:
            raise PermissionError("Acesso negado: Você não pode editar o item de outro usuário.")

        return ItemPerdidoRepository.atualizar_item(item, dados)

    @staticmethod
    def deletar_item_perdido(item_id, current_user):
        item = ItemPerdidoRepository.buscar_por_id(item_id)
        if not item:
            raise ValueError("Erro: Item perdido não encontrado!")

        if item.usuario_id != current_user.id and not current_user.is_admin:
            raise PermissionError("Acesso negado: Você não pode excluir o item de outro usuário.")

        ItemPerdidoRepository.deletar_item(item)
        return True
