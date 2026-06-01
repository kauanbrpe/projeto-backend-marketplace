from flask import Blueprint, jsonify, request
from app.service.cart_service import CartService

cart_bp = Blueprint('cart_bp', __name__, url_prefix='/carts')

@cart_bp.route('/<int:user_id>', methods=['GET'])
def obter_carrinho(user_id):
    carrinho = CartService.obter_por_usuario(user_id)
    if carrinho is None:
        return jsonify({"erro": "Carrinho nao encontrado"}), 404
    return jsonify(carrinho.to_dict()), 200

@cart_bp.route('/adicionar', methods=['POST'])
def adicionar_item():
    data = request.get_json()
    
    if not data or 'user_id' not in data or 'product_id' not in data or 'quantity' not in data:
        return jsonify({"erro": "Dados do carrinho incompletos"}), 400
        
    
    carrinho_atualizado = CartService.adicionar_produto(
        data['user_id'], 
        data['product_id'], 
        data['quantity']
    )
    
    if carrinho_atualizado is False:
        return jsonify({"erro": "Quantidade solicitada excede o estoque disponivel"}), 400
        
    return jsonify(carrinho_atualizado.to_dict()), 200