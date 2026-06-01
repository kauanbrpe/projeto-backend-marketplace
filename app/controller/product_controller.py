from flask import Blueprint, jsonify, request
from app.service.product_service import ProductService

product_bp = Blueprint('product_bp', __name__, url_prefix='/products')

@product_bp.route('/', methods=['GET'])
def listar_produtos():
    produtos = ProductService.listar_todos()
    resultado = []
    for p in produtos:
        resultado.append(p.to_dict())
    return jsonify(resultado), 200

@product_bp.route('/', methods=['POST'])
def cadastrar_produto():
    data = request.get_json()
    
    if not data or 'name' not in data or 'price' not in data or 'category_id' not in data:
        return jsonify({"erro": "Campos obrigatorios ausentes para o produto"}), 400
        
    preco = float(data['price'])
    
    
    if preco <= 0:
        return jsonify({"erro": "O preco do produto deve ser maior que zero"}), 400
        
    novo_produto = ProductService.criar_produto(
        data['name'], 
        preco, 
        data['category_id']
    )
    return jsonify(novo_produto.to_dict()), 201