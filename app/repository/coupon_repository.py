
from app.models.coupon import Coupon
from app import db

class CouponRepository:
    @staticmethod
    def buscar_por_codigo(codigo):
        return Coupon.query.filter_by(codigo=codigo).first()

    @staticmethod
    def salvar(coupon):
        db.session.add(coupon)
        db.session.commit()
        return coupon