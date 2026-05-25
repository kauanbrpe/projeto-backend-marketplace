from flask import Blueprint, jsonify, request
from app.service.order_service import OrderService

order_bp = Blueprint('order_bp', __name__, url_prefix='/orders')

@order_bp.route('/usuario/<int:user_id>', methods=['GET'])
def listar_pedidos(user_id):
    pedidos = OrderService.listar_por_usuario(user_id)
    resultado = []
    for p in pedidos:
        resultado.append(p.to_dict())
    return jsonify(resultado), 200

@order_bp.route('/', methods=['POST'])
def cadastrar_pedido():
    data = request.get_json()
    if not data or 'user_id' not in data or 'itens' not in data or 'total' not in data:
        return jsonify({"erro": "Dados incompletos"}), 400
        
    novo_pedido = OrderService.criar_pedido(data['user_id'], data['itens'], data['total'])
    return jsonify(novo_pedido.to_dict()), 201

@order_bp.route('/<int:order_id>/status', methods=['PUT'])
def alterar_status(order_id):
    data = request.get_json()
    if not data or 'status' not in data:
        return jsonify({"erro": "Status nao informado"}), 400
        
    pedido_atualizado = OrderService.atualizar_status(order_id, data['status'])
    
    if pedido_atualizado is None:
        return jsonify({"erro": "Pedido nao encontrado"}), 404
        
    if pedido_atualizado is False:
        return jsonify({"erro": "Mudanca de status invalida pelas regras de negocio"}), 400
        
    return jsonify(pedido_atualizado.to_dict()), 200