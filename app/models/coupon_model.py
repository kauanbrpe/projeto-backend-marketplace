from app import db
from datetime import datetime

class CouponModel(db.Model):
    __tablename__ = 'coupons'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    discount_type = db.Column(db.String(20), nullable=False, default='fixed')
    discount_value = db.Column(db.Numeric(precision=1, scale=2), nullable=False)
    min_order_value = db.Column(db.Numeric(precision=10, scale=2), default=0.00, nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)
    max_uses = db.Column(db.Integer, default=100, nullable=False)
    used_count = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def is_valid(self, current_total=0):
        now = datetime.now()
        if not self.is_active:
            return False
        if now > self.expiration_date:
            return False
        if self.used_count >= self.max_uses:
            return False
        if current_total < self.min_order_value:
            return False
        return True

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "discount_type": self.discount_type,
            "discount_value": self.discount_value,
            "min_order_value": float(self.min_order_value),
            "expiration_date": self.expiration_date.isoformat(),
            "max_uses": self.max_uses,
            "used_count": self.used_count,
            "is_active": self.is_active
        }