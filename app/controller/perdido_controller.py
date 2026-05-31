from flask import Blueprint, jsonify, request
from app.service.perdido_service import PerdidoService

perdido_bp = Blueprint('perdido_bp', __name__, url_prefix='/perdidos')

@perdido_bp.route('/', methods=['GET'])
def listar():
    lista = PerdidoService.listar_todos()
    resultado = []
    for p in lista:
        resultado.append(p.to_dict())
    return jsonify(resultado), 200

@perdido_bp.route('/', methods=['POST'])
def cadastrar():
    data = request.get_json()
    
    if not data or 'nome' not in data or 'descricao' not in data:
        return jsonify({"erro": "Nome e descricao sao obrigatorios"}), 400
        
    novo = PerdidoService.criar_perdido(data['nome'], data['descricao'])
    return jsonify(novo.to_dict()), 201