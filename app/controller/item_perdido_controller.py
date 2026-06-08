from flask import request
from flask_restx import Namespace, Resource, fields
from flask_login import login_required, current_user
from app.service import ItemPerdidoService

item_perdido_ns = Namespace("itensperdidos", description="Operações relacionadas aos Items Perdidos")

item_perdido_input_schema = item_perdido_ns.model('ItemPerdidoInput', {
    'nome_item': fields.String(required=True, description='Nome do item perdido', example='Chaveiro de couro'),
    'descricao': fields.String(required=True, description='Descrição detalhada do item', example='Chaveiro preto com 3 chaves'),
    'local_perdido': fields.String(required=True, description='Local onde o item foi perdido', example='Estacionamento Bloco B'),
    'data_perdido': fields.String(required=True, description='Data em que foi perdido (AAAA-MM-DD)', example='2026-06-02'),
    'perdido_id': fields.Integer(required=True, description='ID do registro de Perdido vinculado', example=1)
})

item_perdido_update_schema = item_perdido_ns.model('ItemPerdidoUpdateInput', {
    'nome_item': fields.String(required=False, description='Novo nome do item'),
    'descricao': fields.String(required=False, description='Nova descrição'),
    'local_perdido': fields.String(required=False, description='Novo local'),
    'data_perdido': fields.String(required=False, description='Nova data (AAAA-MM-DD)'),
    'perdido_id': fields.Integer(required=False, description='Novo ID do Perdido')
})

item_perdido_output_schema = item_perdido_ns.model('ItemPerdidoOutput', {
    'id': fields.Integer(description='ID único do item perdido'),
    'nome_item': fields.String(description='Nome do item'),
    'descricao': fields.String(description='Descrição'),
    'local_perdido': fields.String(description='Local'),
    'data_perdido': fields.String(description='Data'),
    'perdido_id': fields.Integer(description='ID do Perdido associado'),
    'usuario_id': fields.Integer(description='ID do usuário que registrou')
})

@item_perdido_ns.route('/')
class ItemPerdidoList(Resource):

    @item_perdido_ns.doc(responses={200: 'Ok'})
    @item_perdido_ns.marshal_list_with(item_perdido_output_schema)
    def get(self):
        try:
            return ItemPerdidoService.listar_todos(), 200
        except Exception as e:
            return {"error": "Erro interno ao listar os itens perdidos."}, 500

    @item_perdido_ns.expect(item_perdido_input_schema)
    @item_perdido_ns.doc(responses={201: 'Created', 400: 'Invalid', 401: 'Unauthorized'})
    @login_required
    def post(self):
        data = request.json

        field_required = ['nome_item', 'descricao', 'local_perdido', 'data_perdido', 'perdido_id']
        if not data or not all(field in data for field in field_required):
            return {"error": "Dados incompletos. Todos os campos obrigatórios devem ser preenchidos."}, 400

        try:
            data['usuario_id'] = current_user.id
            new_item = ItemPerdidoService.criar_item_perdido(data)
            return new_item.to_dict(), 201
        except Exception as e:
            return {"error": "Erro interno ao cadastrar o item perdido."}, 500

@item_perdido_ns.route('/<int:item_id>')
@item_perdido_ns.doc(params={'item_id': 'O identificador único do item perdido'})
class ItemPerdidoDetail(Resource):

    @item_perdido_ns.doc(responses={200: 'Ok', 404: 'Not Found'})
    @item_perdido_ns.marshal_with(item_perdido_output_schema)
    def get(self, item_id):
        item = ItemPerdidoService.listar_por_id(item_id)
        if not item:
            return {"error": "Item perdido não encontrado."}, 404
        return item, 200

    @item_perdido_ns.expect(item_perdido_update_schema)
    @item_perdido_ns.doc(responses={200: 'Ok', 400: 'Invalid', 401: 'Unauthorized', 403: 'Forbidden', 404: 'Not Found'})
    @login_required
    def put(self, item_id):
        data = request.json
        if not data:
            return {"error": "Nenhum dado enviado para atualização."}, 400

        try:
            updated = ItemPerdidoService.atualizar_item_perdido(item_id, data, current_user)
            return updated.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 404
        except PermissionError as e:
            return {"error": str(e)}, 403
        except Exception as e:
            return {"error": "Erro interno ao atualizar o item perdido."}, 500

    @item_perdido_ns.doc(responses={200: 'Ok', 401: 'Unauthorized', 403: 'Forbidden', 404: 'Not Found'})
    @login_required
    def delete(self, item_id):
        try:
            ItemPerdidoService.deletar_item_perdido(item_id, current_user)
            return {"message": "Item perdido excluído com sucesso."}, 200
        except ValueError as e:
            return {"error": str(e)}, 404
        except PermissionError as e:
            return {"error": str(e)}, 403
        except Exception as e:
            return {"error": "Erro interno ao excluir o item perdido."}, 500

@item_perdido_ns.route('/usuario/<int:user_id>')
@item_perdido_ns.doc(params={'user_id': 'O identificador único do usuário'})
class ItemPerdidoDetailUser(Resource):

    @item_perdido_ns.doc(responses={200: 'Ok', 404: 'Not Found'})
    @item_perdido_ns.marshal_list_with(item_perdido_output_schema)
    def get(self, user_id):
        items = ItemPerdidoService.listar_por_usuario_id(user_id)
        if not items:
            return {"error": "Usuário não tem itens perdidos."}, 404
        return items, 200
