from flask import request
from flask_restx import Namespace, Resource, fields
from flask_login import login_required, current_user
from app.service import PaymentService
from app.models import OrderModel

payment_ns = Namespace('payments', description='Operações relacionadas ao processamento de pagamentos')

payment_input_schema = payment_ns.model('PaymentInput', {
    'order_id': fields.Integer(required=True, description='ID do pedido a ser pago', example=1),
    'metodo_pagamento': fields.String(required=True, description='Método utilizado (credit_card, pix, boleto)', example='pix'),
    'valor': fields.Float(required=True, description='Valor enviado para pagamento', example=150.00)
})

payment_output_schema = payment_ns.model('PaymentOutput', {
    'id': fields.Integer(description='ID único do registro de pagamento'),
    'order_id': fields.Integer(description='ID do pedido associado'),
    'payment_method': fields.String(description='Método de pagamento utilizado'),
    'status': fields.String(description='Status da transação (Aprovado, Pendente, Falhou)'),
    'amount_paid': fields.Float(description='Valor efetivamente pago'),
    'transaction_id': fields.String(description='ID único da transação gerado pelo gateway')
})

@payment_ns.route('/')
class PaymentProcess(Resource):

    @payment_ns.expect(payment_input_schema)
    @payment_ns.doc(responses={201: "Created", 400: 'Invalid', 403: 'Access Denied', 404: 'Not Found'})
    @login_required
    def post(self):
        data = request.json

        if not data or 'order_id' not in data or 'metodo_pagamento' not in data or 'valor' not in data:
            return {"error": "Dados de pagamento incompletos. Todos os campos são obrigatórios."}, 400

        order = OrderModel.query.get(data['order_id'])
        if not order:
            return {"error": "Pedido não encontrado para faturamento."}, 404

        if order.user_id != current_user and not current_user.is_admin:
            return {"error": "Acesso negado: Você não pode pagar um pedido que pertence a outro usuário."}, 403

        try:
            result = PaymentService.processar_pagamento(
                order_id=data['order_id'],
                metodo_pagamento=data['metodo_pagamento'],
                valor=data['valor']
            )

            if result is None:
                return {"error": "Erro ao localizar o pedido informado."}, 404

            if result is False:
                return {
                    "error": f"Erro no pagamento: O valor enviado (R$ {data['valor']:.2f}) é menor do que o total do pedido (R$ {float(order.total_price):.2f})."}, 400

            return result.to_dict(), 201

        except Exception as e:
            return {"error": "Erro interno ao processar a transação financeira."}, 500

@payment_ns.route('/<int:payment_id>')
@payment_ns.doc(params={'payment_id': 'O identificador único do pagamento'})
class PaymentDetail(Resource):

    @payment_ns.doc(responses={200: 'Ok', 403: 'Access Denied', 404: 'Not Found'})
    @payment_ns.marshal_with(payment_output_schema)
    @login_required
    def get(self,payment_id):
        payment = PaymentService.obter_por_id(payment_id)

        if not payment:
            return {"error": "Registro de pagamento não encontrado."}, 404

        order = OrderModel.query.get(payment.order_id)
        
        if order and order.user_id != current_user.id and not current_user.is_admin:
            return {"error": "Acesso negado: Este registro pertence à transação de outro usuário."}, 403

        return payment, 200