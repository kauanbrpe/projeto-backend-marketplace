from app.models.payment import Payment
from app import db

class PaymentRepository:
    @staticmethod
    def salvar(payment):
        db.session.add(payment)
        db.session.commit()
        return payment

    @staticmethod
    def buscar_por_id(payment_id):
        return Payment.query.get(payment_id)