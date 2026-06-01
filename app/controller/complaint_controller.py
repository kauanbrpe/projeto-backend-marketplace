from flask import Blueprint, jsonify, request
from app.service.complaint_service import ComplaintService

complaint_bp = Blueprint('complaint_bp', __name__, url_prefix='/complaints')

@complaint_bp.route('/', methods=['POST'])
def cadastrar_reclamacao():
    data = request.get_json()
    
    if not data or 'order_id' not in data or 'description' not in data:
        return jsonify({"erro": "Pedido e descricao sao obrigatorios"}), 400
        
    resultado = ComplaintService.abrir_reclamacao(data['order_id'], data['description'])
    
    if resultado is None:
        return jsonify({"erro": "Pedido nao encontrado"}), 404
        
    if resultado is False:
        return jsonify({"erro": "Reclamacoes so podem ser abertas para pedidos entregues"}), 400
        
    return jsonify(resultado.to_dict()), 201