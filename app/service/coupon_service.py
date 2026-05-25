from datetime import datetime
from app import db
from app.models.coupon_model import CouponModel

class CouponService:
    @staticmethod
    def obter_por_id(coupon_id):
        return CouponModel.query.get(coupon_id)

    @staticmethod
    def validar_e_calcular_desconto(codigo, valor_total_pedido):
        cupom = CouponModel.query.filter_by(code=codigo).first()
        
        if not cupom:
            return None  
            
        
        if not cupom.is_active:
            return None
            
        
        if datetime.now() > cupom.expiration_date:
            return None
            
        
        if cupom.used_count >= cupom.max_uses:
            return None
            
        
        if valor_total_pedido < cupom.min_order_value:
            return None
            
        
        if cupom.discount_type == "percent":
            desconto = valor_total_pedido * (cupom.discount_value / 100)
        else:
            desconto = cupom.discount_value
            
        return desconto

    @staticmethod
    def incrementar_uso(coupon_id):
        cupom = CouponModel.query.get(coupon_id)
        if cupom:
            cupom.used_count = cupom.used_count + 1  # Incremento simples [cite: 223]
            db.session.commit()
            return True
        return False