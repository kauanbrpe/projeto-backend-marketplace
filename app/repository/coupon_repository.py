from app import db
from app.models import CouponModel

class CouponRepository:
    @staticmethod
    def save(coupon):
        db.session.add(coupon)
        db.session.commit()
        return coupon

    @staticmethod
    def find_by_code(code):
        return CouponModel.query.filter_by(code=code.upper()).first()

    @staticmethod
    def find_by_id(coupon_id):
        return CouponModel.query.get(coupon_id)

    @staticmethod
    def find_all():
        return CouponModel.query.all()

    @staticmethod
    def delete(coupon):
        db.session.delete(coupon)
        db.session.commit()
        return True
