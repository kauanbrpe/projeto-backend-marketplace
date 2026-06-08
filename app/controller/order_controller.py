from flask import request
from flask_restx import Namespace, Resource, fields
from flask_login import login_required, current_user
from app.service import OrderService

order_ns = Namespace('orders', description='Operações relacionadas ao gerenciamento de pedidos')

item_pedido_schema = order_ns.model('OrderItemInput', {
    'product_id': fields.Integer(required=True, description='ID do produto'),
    'quantity': fields.Integer(required=True, description='Quantidade comprada'),
    'price_at_purchase': fields.Float(required=True, description='Preço unitário no momento da compra')
})

order_input_schema = order_ns.model('OrderCreateInput', {
    'itens': fields.List(fields.Nested(item_pedido_schema), required=True, description='Lista de itens do carrinho'),
    'valor_total': fields.Float(required=True, description='Valor total cobrado pelo pedido')
})

order_status_schema = order_ns.model('OrderStatusUpdateInput', {
    'status': fields.String(required=True, description='Novo status do pedido (Pago, Enviado, Cancelado)', example='Pago')
})

@order_ns.route('/')
class OrderList(Resource):

    @order_ns.doc(responses={200: 'Ok', 401: 'Unauthorized'})
    @login_required
    def get(self):
        try:
            orders = OrderService.listar_por_usuario(current_user.id)
            return [order.to_dict() for order in orders], 200
        except Exception as e:
            return {"error": "Erro interno ao buscar histórico de pedidos"}, 500

    @order_ns.expect(order_input_schema)
    @order_ns.doc(responses={201: 'Created', 400: 'Invalid', 401: 'Unauthorized'})
    @login_required
    def post(self):
        data = request.json

        if not data or 'itens' not in data or 'valor_total' not in data:
            return {"error": "Dados de pedido incompletos"}, 400

        try:
            new_order = OrderService.criar_pedido(
                user_id=current_user.id,
                itens_carrinho=data['itens'],
                valor_total=data['valor_total']
            )
            return new_order.to_dict(), 201
        except Exception as e:
            return {"error": "Erro interno ao processar e fechar o pedido"}, 500

@order_ns.route('/<int:order_id>')
@order_ns.doc(params={'order_id': 'O identificador único do pedido'})
class OrderDetail(Resource):

    @order_ns.doc(responses={200: 'Ok', 403: 'Access prohibited', 404: 'Not found'})
    @login_required
    def get(self, order_id):
        order = OrderService.obter_por_id(order_id)

        if not order:
            return {"error": "Pedido não encontrado"}, 404
        if order.user_id != current_user.id and not current_user.is_admin:
            return {"error": "Acesso negado: Este pedido pertence a outro usuário."}, 403

        return order.to_dict(), 200

    @order_ns.expect(order_status_schema)
    @order_ns.doc(responses={200: 'Ok', 400: 'Invalid', 403: 'Access prohibited', 404: 'Not found'})
    @login_required
    def put(self, order_id):
        if not current_user.is_admin:
            return {"error": "Acesso negado: Apenas administradores podem alterar o status de um pedido."}, 403

        data = request.json
        if not data or 'status' not in data:
            return {"error": "O campo 'status' é obrigatório"}, 400

        pedido_atualizado = OrderService.atualizar_status(order_id, data['status'])

        if pedido_atualizado is None:
            return {"error": "Pedido não encontrado"}, 404

        if pedido_atualizado is False:
            return {"error": f"Mudança de status inválida para as regras de negócio de fluxo do pedido ({data['status']})."}, 400

        return pedido_atualizado.to_dict(), 200

    @order_ns.doc(responses={200: 'Ok', 401: 'Unauthorized', 403: 'Forbidden', 404: 'Not Found'})
    @login_required
    def delete(self, order_id):
        try:
            OrderService.deletar_pedido(order_id, current_user)
            return {"message": "Pedido excluído com sucesso."}, 200
        except ValueError as e:
            return {"error": str(e)}, 404
        except PermissionError as e:
            return {"error": str(e)}, 403
        except Exception as e:
            return {"error": "Erro interno ao excluir o pedido."}, 500
