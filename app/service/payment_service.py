from app.models.payment_model import PaymentModel
import uuid
from app.repository import PaymentRepository, OrderRepository

class PaymentService:
    @staticmethod
    def obter_por_id(payment_id):
        return PaymentRepository.find_by_id(payment_id)

    @staticmethod
    def processar_pagamento(order_id, metodo_pagamento, valor):
        pedido = OrderRepository.buscar_por_id(order_id)

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

        pedido.status = "Pago"

        return PaymentRepository.save(novo_pagamento)

    @staticmethod
    def atualizar_pagamento(payment_id, dados, current_user):
        payment = PaymentRepository.find_by_id(payment_id)
        if not payment:
            raise ValueError("Erro: Pagamento não encontrado!")

        if not current_user.is_admin:
            raise PermissionError("Acesso negado: Apenas administradores podem atualizar pagamentos.")

        if 'status' in dados:
            payment.status = dados['status']
        if 'payment_method' in dados:
            payment.payment_method = dados['payment_method']

        return PaymentRepository.update(payment)

    @staticmethod
    def deletar_pagamento(payment_id, current_user):
        payment = PaymentRepository.find_by_id(payment_id)
        if not payment:
            raise ValueError("Erro: Pagamento não encontrado!")

        if not current_user.is_admin:
            raise PermissionError("Acesso negado: Apenas administradores podem excluir pagamentos.")

        PaymentRepository.delete(payment)
        return True
