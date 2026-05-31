from flask import Blueprint, jsonify, request
from app.service.user_service import UserService

user_bp = Blueprint('user_bp', __name__, url_prefix='/users')

@user_bp.route('/<int:user_id>', methods=['GET'])
def obter_usuario(user_id):
    usuario = UserService.obter_por_id(user_id)
    if usuario is None:
        return jsonify({"erro": "Usuario nao encontrado"}), 404
    return jsonify(usuario.to_dict()), 200

@user_bp.route('/', methods=['POST'])
def cadastrar_usuario():
    data = request.get_json()
    
    if not data or 'nome' not in data or 'email' not in data or 'senha' not in data or 'tipo' not in data:
        return jsonify({"erro": "Dados obrigatorios do usuario ausentes"}), 400
        
    tipo_usuario = data['tipo']
    
  
    if tipo_usuario != 'Cliente':
        if tipo_usuario != 'Vendedor':
            return jsonify({"erro": "Tipo de usuario deve ser Cliente ou Vendedor"}), 400
            
    
    novo_usuario = UserService.criar_usuario(data)
    
    if novo_usuario is None:
        return jsonify({"erro": "E-mail ja cadastrado no sistema"}), 400
        
    return jsonify(novo_usuario.to_dict()), 201