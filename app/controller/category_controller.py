from flask import Blueprint, jsonify, request
from app.service.category_service import CategoryService

category_bp = Blueprint('category_bp', __name__, url_prefix='/categories')

@category_bp.route('/', methods=['GET'])
def listar_categorias():
    categorias = CategoryService.listar_todas()
    resultado = []
    for c in categorias:
        resultado.append(c.to_dict())
    return jsonify(resultado), 200

@category_bp.route('/', methods=['POST'])
def cadastrar_categoria():
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({"erro": "Nome da categoria e obrigatorio"}), 400
        
    nova_categoria = CategoryService.criar_categoria(data['name'])
    return jsonify(nova_categoria.to_dict()), 201