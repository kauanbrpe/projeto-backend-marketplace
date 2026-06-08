from flask import request
from flask_restx import Namespace, Resource, fields
from flask_login import login_required, current_user
from app.service import PerdidoService

perdido_ns = Namespace("perdidos", description="Operações relacionadas à perdidos")

perdido_input_schema = perdido_ns.model('PerdidoInput', {
    'nome': fields.String(required=True, description='Nome do perdido'),
    'descricao': fields.String(required=True, description='Descrição do Perdido')
})

perdido_update_schema = perdido_ns.model('PerdidoUpdateInput', {
    'nome': fields.String(required=False, description='Novo nome'),
    'descricao': fields.String(required=False, description='Nova descrição')
})

perdido_output_schema = perdido_ns.model('PerdidoOutput', {
    'id': fields.Integer(description='ID do Perdido'),
    'nome': fields.String(description='Nome do Perdido'),
    'descricao': fields.String(description='Descrição do Perdido'),
})

@perdido_ns.route('/')
class PerdidoList(Resource):

    @perdido_ns.doc(responses={200: 'Ok'})
    @perdido_ns.marshal_list_with(perdido_output_schema)
    def get(self):
        try:
            return PerdidoService.listar_todos(), 200
        except Exception as e:
            return {"error": "Erro interno ao listar os perdidos."}, 500

    @perdido_ns.expect(perdido_input_schema)
    @perdido_ns.doc(responses={201: 'Created', 400: 'Invalid', 401: 'Unauthorized'})
    @login_required
    def post(self):
        data = request.json

        try:
            new_item = PerdidoService.criar_perdido(
                nome=data['nome'],
                descricao=data['descricao'],
            )
            return new_item.to_dict(), 201
        except Exception as e:
            return {"error": "Erro interno ao cadastrar o perdido."}, 500

@perdido_ns.route('/<int:perdido_id>')
@perdido_ns.doc(params={'perdido_id': 'O identificador único do perdido'})
class PerdidoDetail(Resource):

    @perdido_ns.doc(responses={200: 'Ok', 404: 'Not Found'})
    @perdido_ns.marshal_with(perdido_output_schema)
    def get(self, perdido_id):
        item = PerdidoService.listar_por_id(perdido_id)
        if not item:
            return {"error": "Perdido não encontrado."}, 404
        return item, 200

    @perdido_ns.expect(perdido_update_schema)
    @perdido_ns.doc(responses={200: 'Ok', 400: 'Invalid', 401: 'Unauthorized', 404: 'Not Found'})
    @login_required
    def put(self, perdido_id):
        data = request.json
        if not data:
            return {"error": "Nenhum dado enviado para atualização."}, 400

        try:
            updated = PerdidoService.atualizar_perdido(perdido_id, data)
            return updated.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 404
        except Exception as e:
            return {"error": "Erro interno ao atualizar o perdido."}, 500

    @perdido_ns.doc(responses={200: 'Ok', 401: 'Unauthorized', 404: 'Not Found'})
    @login_required
    def delete(self, perdido_id):
        try:
            PerdidoService.deletar_perdido(perdido_id)
            return {"message": "Perdido excluído com sucesso."}, 200
        except ValueError as e:
            return {"error": str(e)}, 404
        except Exception as e:
            return {"error": "Erro interno ao excluir o perdido."}, 500
