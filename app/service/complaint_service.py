from app import db
from app.models.complaint_model import ComplaintModel
from app.models.order_model import OrderModel

class ComplaintService:
    @staticmethod
    def abrir_reclamacao(order_id, descricao):
        pedido = OrderModel.query.get(order_id)
        
        
        if not pedido:
            return None
            
        
        if pedido.status != "Entregue":
            return False
            
        nova_reclamacao = ComplaintModel(
            order_id=order_id,
            description=descricao,
            status="Aberta"
        )
        
        db.session.add(nova_reclamacao)
        db.session.commit()
        return nova_reclamacao