from app.models.order_model import OrderModel, OrderItemModel
from app import db

class OrderRepository:

    @staticmethod
    def criar_pedido(data):
        novo_pedido = OrderModel(
            user_id=data['user_id'],
            status=data.get('status', 'pending'),
            total_price=data.get('total_price', 0.00),
            coupon_id=data.get('coupon_id')
        )

        db.session.add(novo_pedido)
        db.session.flush()

        itens = data.get('items', [])

        for item in itens:
            novo_item = OrderItemModel(
                order_id=novo_pedido.id,
                product_id=item['product_id'],
                quantity=item['quantity'],
                historic_price=item['historic_price']
            )

            db.session.add(novo_item)

        db.session.commit()

        return novo_pedido

    @staticmethod
    def listar_pedidos():
        return OrderModel.query.all()

    @staticmethod
    def buscar_por_id(order_id):
        return db.session.get(OrderModel, order_id)

    @staticmethod
    def listar_por_usuario(user_id):
        return OrderModel.query.filter_by(user_id=user_id).all()

    @staticmethod
    def atualizar_status(order, novo_status):
        order.status = novo_status

        db.session.commit()

        return order

    @staticmethod
    def deletar_pedido(order):
        db.session.delete(order)
        db.session.commit()
        return True