from app import db
from app.models.order_model import OrderModel, OrderItemModel
from app.repository import OrderRepository

class OrderService:
    @staticmethod
    def obter_por_id(order_id):
        return OrderRepository.buscar_por_id(order_id)

    @staticmethod
    def listar_por_usuario(user_id):
        return OrderRepository.listar_por_usuario(user_id)

    @staticmethod
    def criar_pedido(user_id, itens_carrinho, valor_total):
        
        novo_pedido = OrderModel(
            user_id=user_id,
            status="Criado",
            total_price=valor_total
        )
        db.session.add(novo_pedido)
        db.session.flush()
        
        
        for item in itens_carrinho:
            item_pedido = OrderItemModel(
                order_id=novo_pedido.id,
                product_id=item['product_id'],
                quantity=item['quantity'],
                historic_price=item['price_at_purchase']
            )
            db.session.add(item_pedido)
            
        return OrderRepository.criar_pedido(novo_pedido)

    @staticmethod
    def atualizar_status(order_id, novo_status):
        pedido = OrderRepository.buscar_por_id(order_id)
        if not pedido:
            return None
            
        
        if novo_status == "Enviado" and pedido.status != "Pago":
            return False
            
        
        if novo_status == "Cancelado" and pedido.status == "Enviado":
            return False
            
        pedido.status = novo_status
        return OrderRepository.atualizar_status(novo_status, pedido)