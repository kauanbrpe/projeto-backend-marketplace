from flask import Blueprint, jsonify, request
from app.service.coupon_service import CouponService

coupon_bp = Blueprint('coupon_bp', __name__, url_prefix='/coupons')

@coupon_bp.route('/validar', methods=['POST'])
def validar_cupom():
    data = request.get_json()
    
    if not data or 'code' not in data or 'total' not in data:
        return jsonify({"erro": "Dados obrigatorios faltando"}), 400
        
    codigo = data['code']
    total_pedido = float(data['total'])
    
    desconto = CouponService.validar_e_calcular_desconto(codigo, total_pedido)
    
    if desconto is None:
        return jsonify({"erro": "Cupom invalido ou expirado"}), 400
        
    return jsonify({"desconto": desconto}), 200