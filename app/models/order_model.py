from app import db
from datetime import datetime

class OrderItemModel(db.Model):
    __tablename__ = 'order_items'

    order_id = db.Column(db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    historic_price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)

class OrderModel(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50), default='pending', nullable=False)
    total_price = db.Column(db.Numeric(precision=10, scale=2), nullable=False, default=0.00)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    items = db.relationship('OrderItemModel', backref='order', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "status": self.status,
            "total_price": self.total_price,
            "created_at": self.created_at.isoformat(),
            "items": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price_at_purchase": float(item.historic_price)
                } for item in self.items
            ]
        }