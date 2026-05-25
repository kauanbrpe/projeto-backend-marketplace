from flask import Blueprint, jsonify, request
from app.service.review_service import ReviewService

review_bp = Blueprint('review_bp', __name__, url_prefix='/reviews')

@review_bp.route('/produto/<int:product_id>', methods=['GET'])
def listar_por_produto(product_id):
    avaliacoes = ReviewService.listar_por_produto(product_id)
    resultado = []
    for r in avaliacoes:
        resultado.append(r.to_dict())
    return jsonify(resultado), 200

@review_bp.route('/', methods=['POST'])
def cadastrar_review():
    data = request.get_json()
    
    if not data or 'user_id' not in data or 'product_id' not in data or 'rating' not in data:
        return jsonify({"erro": "Dados obrigatorios ausentes"}), 400
        
    comentario = ""
    if 'comment' in data:
        comentario = data['comment']
        
    nova = ReviewService.criar_avaliacao(
        data['user_id'], 
        data['product_id'], 
        data['rating'], 
        comentario
    )
    
    if nova is False:
        return jsonify({"erro": "A nota deve ser um numero inteiro entre 1 e 5"}), 400
        
    return jsonify(nova.to_dict()), 201