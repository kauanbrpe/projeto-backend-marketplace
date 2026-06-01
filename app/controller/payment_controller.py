from flask import Blueprint, jsonify, request
from app.service.payment_service import PaymentService

payment_bp = Blueprint('payment_bp', __name__, url_prefix='/payments')

@payment_bp.route('/processar', methods=['POST'])
def processar_pagamento():
    data = request.get_json()
    
    if not data or 'order_id' not in data or 'metodo_pagamento' not in data:
        return jsonify({"erro": "Campos obrigatorios ausentes"}), 400
        
    metodo = data['metodo_pagamento']
    
    if metodo != 'Cartão de Crédito':
        if metodo != 'Pix':
            if metodo != 'Boleto Bancário':
                return jsonify({"erro": "Metodo de pagamento invalido"}), 400
                
    if metodo == 'Cartão de Crédito':
        if 'numero_cartao' not in data or 'nome_titular' not in data or 'validade' not in data or 'cvv' not in data:
            return jsonify({"erro": "Dados do cartao de credito incompletos"}), 400
            
    
    pagamento = PaymentService.processar_pagamento(
        data['order_id'],
        data['metodo_pagamento'],
        data.get('valor') 
    )
    
    if pagamento is None:
        return jsonify({"erro": "Pedido nao encontrado ou pagamento recusado"}), 404
        
    return jsonify(pagamento.to_dict()), 201