from app.models.complaint_model import ComplaintModel
from app.models.order_model import OrderModel
from app.repository import ComplaintRepository

class ComplaintService:
    @staticmethod
    def listar_todas(current_user):
        if not current_user.is_admin:
            raise PermissionError("Acesso negado: Apenas administradores podem listar todas as reclamações.")
        return ComplaintRepository.find_all()

    @staticmethod
    def listar_por_usuario(user_id):
        return ComplaintRepository.find_by_user_id(user_id)

    @staticmethod
    def listar_por_id(complaint_id):
        return ComplaintRepository.find_by_id(complaint_id)

    @staticmethod
    def abrir_reclamacao(user, order_id, descricao):
        pedido = OrderModel.query.get(order_id)

        if not pedido:
            return None

        if pedido.status != "Entregue":
            return False

        nova_reclamacao = ComplaintModel(
            user_id=user.id,
            order_id=order_id,
            description=descricao,
            status="Aberta"
        )

        return ComplaintRepository.save(nova_reclamacao)

    @staticmethod
    def atualizar_reclamacao(complaint_id, dados, current_user):
        reclamacao = ComplaintRepository.find_by_id(complaint_id)
        if not reclamacao:
            raise ValueError("Erro: Reclamação não encontrada!")

        if reclamacao.user_id != current_user.id and not current_user.is_admin:
            raise PermissionError("Acesso negado: Você não pode editar a reclamação de outro usuário.")

        if 'description' in dados:
            reclamacao.description = dados['description']
        if 'status' in dados and current_user.is_admin:
            reclamacao.status = dados['status']

        return ComplaintRepository.update(reclamacao)

    @staticmethod
    def deletar_reclamacao(complaint_id, current_user):
        reclamacao = ComplaintRepository.find_by_id(complaint_id)
        if not reclamacao:
            raise ValueError("Erro: Reclamação não encontrada!")

        if reclamacao.user_id != current_user.id and not current_user.is_admin:
            raise PermissionError("Acesso negado: Você não pode excluir a reclamação de outro usuário.")

        ComplaintRepository.delete(reclamacao)
        return True
