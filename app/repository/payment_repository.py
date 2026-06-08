from app import db
from app.models import PaymentModel

class PaymentRepository:
    @staticmethod
    def save(payment):
        db.session.add(payment)
        db.session.commit()
        return payment

    @staticmethod
    def find_by_id(payment_id):
        return PaymentModel.query.get(payment_id)

    @staticmethod
    def find_by_order_id(order_id):
        return PaymentModel.query.filter_by(order_id=order_id).first()

    @staticmethod
    def update(payment):
        db.session.add(payment)
        db.session.commit()
        return payment

    @staticmethod
    def delete(payment):
        db.session.delete(payment)
        db.session.commit()
        return True
