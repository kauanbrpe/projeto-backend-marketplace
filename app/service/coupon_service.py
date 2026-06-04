from datetime import datetime
from app import db
from app.repository import CouponRepository
from app.models.coupon_model import CouponModel

class CouponService:
    @staticmethod
    def listar_todos(current_user):
        if not current_user.is_authenticated or not current_user.is_admin:
            raise PermissionError("Permission denied.")

        cupons = CouponModel.query.all()
        return [cupom.to_dict() for cupom in cupons]

    @staticmethod
    def criar_cupom(data, current_user):
        if not current_user.is_authenticated or not current_user.is_admin:
            raise PermissionError("Permission denied.")

        if not data.get('code') or not data.get('discount_type') or not data.get('discount_value') or not data.get('expiration_date'):
            raise ValueError("Required fields")

        coupom_existente = CouponRepository.find_by_code(data['code'])
        if coupom_existente:
            raise ValueError("Error: A coupon with this code has already been registered!")

        try:
            data_expiracao = datetime.strptime(data['expiration_date'], '%Y-%m-%d')
        except ValueError:
            raise ValueError("Error: Invalid date format! Use the YYYY-MM-DD format.")

        new_coupon = CouponModel(
            code=data['code'].upper(),
            discount_type=data['discount_type'],
            discount_value=data['discount_value'],
            min_order_value=data.get('min_order_value', 0.00),
            max_uses=data.get('max_uses', 100),
            expiration_date=data_expiracao,
            is_active=data.get('is_active', True)
        )

        return CouponRepository.save(new_coupon)

    @staticmethod
    def obter_por_id(coupon_id):
        return CouponModel.query.get(coupon_id)

    @staticmethod
    def validar_e_calcular_desconto(codigo, valor_total_pedido):
        cupom = CouponRepository.find_by_code(codigo).first
        
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
        cupom = CouponRepository.find_by_id(coupon_id)
        if cupom:
            cupom.used_count = cupom.used_count + 1  # Incremento simples [cite: 223]
            db.session.commit()
            return True
        return False