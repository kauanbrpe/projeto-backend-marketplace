from app import db
from datetime import datetime

class PaymentModel(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), unique=True, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='pending', nullable=False)
    amount_paid = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    gateway_transaction_id = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "payment_method": self.payment_method,
            "status": self.status,
            "amount_paid": float(self.amount_paid),
            "transaction_id": self.gateway_transaction_id,
            "created_at": self.created_at.isoformat()
        }


