from app import db
from app.models.payment_model import PaymentModel
from app.models.order_model import OrderModel
import uuid

class PaymentService:
    @staticmethod
    def obter_por_id(payment_id):
        return PaymentModel.query.get(payment_id)

    @staticmethod
    def processar_pagamento(order_id, metodo_pagamento, valor):
        pedido = OrderModel.query.get(order_id)
        
        
        if not pedido:
            return None  
            
        
        if valor < pedido.total_price:
            return False  
            
        
        novo_pagamento = PaymentModel(
            order_id=order_id,
            payment_method=metodo_pagamento,
            amount_paid=valor,  
            gateway_transaction_id=str(uuid.uuid4()), 
            status="Aprovado"  
        )
        db.session.add(novo_pagamento)
        
        
        pedido.status = "Pago"
        
        db.session.commit()
        return novo_pagamento