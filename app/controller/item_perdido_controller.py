from flask import Blueprint, jsonify, request
from app.service.item_perdido_service import ItemPerdidoService

item_perdido_bp = Blueprint('item_perdido_bp', __name__, url_prefix='/itens-perdidos')

@item_perdido_bp.route('/', methods=['GET'])
def listar():
    itens = ItemPerdidoService.listar_todos()
    resultado = []
    for i in itens:
        resultado.append(i.to_dict())
    return jsonify(resultado), 200

@item_perdido_bp.route('/', methods=['POST'])
def cadastrar():
    data = request.get_json()
    
    
    if not data or 'nome_item' not in data or 'descricao' not in data or 'usuario_id' not in data:
        return jsonify({"erro": "Campos obrigatorios ausentes"}), 400
        
    novo = ItemPerdidoService.criar_item_perdido(data)
    return jsonify(novo.to_dict()), 201