from app.models.complaint_model import ComplaintModel
from app.models.order_model import OrderModel
from app.repository import ComplaintRepository

class ComplaintService:
    @staticmethod
    def abrir_reclamacao(user, order_id, descricao):
        pedido = OrderModel.query.get(order_id)
        user = OrderModel.query.get(user)

        if not pedido:
            return None

        if not user:
            return None

        if pedido.status != "Entregue":
            return False
            
        nova_reclamacao = ComplaintModel(
            user=user,
            order_id=order_id,
            description=descricao,
            status="Aberta"
        )
        
        return ComplaintRepository.save(nova_reclamacao)