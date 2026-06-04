from flask import request
from flask_restx import Namespace, Resource, fields
from flask_login import login_required, current_user
from app.service import PerdidoService

perdido_ns = Namespace("perdidos", description="Operações relacionadas à perdidos")

perdido_input_schema = perdido_ns.model('PerdidoInput', {
    'nome': fields.String(required=True, description='Nome do perdido'),
    'descricao': fields.String(required=True, description='Descrição do Perdido')
})

perdido_output_schema = perdido_ns.model('PerdidoOutput', {
    'id': fields.Integer(required=True, description='ID do Perdido'),
    'nome': fields.String(required=True, description='Nome do Perdido'),
    'descricao': fields.String(required=True, description='Descrição do Perdido'),
})

@perdido_ns.route('/')
class PerdidoList(Resource):

    @perdido_ns.doc(responses={200: 'Ok'})
    @perdido_ns.marshal_list_with(perdido_output_schema)
    def get(self):
        try:
            return PerdidoService.listar_todos(), 200
        except Exception as e:
            return {"error": "Erro interno ao listar os itens perdidos."}, 500

    @perdido_ns.expect(perdido_input_schema)
    @perdido_ns.doc(responses={201: 'Created', 400: 'Invalid', 401: 'Unauthorized'})
    @login_required
    def post(self):
        data = request.json

        try:
            data['usuario_id'] = current_user.id
            new_item = PerdidoService.criar_perdido(
                nome=data['nome'],
                descricao=data['descricao'],
            )
            return new_item.to_dict(), 201
        except Exception as e:
            return {"error": "Erro interno ao cadastrar o item perdido."}, 500

@perdido_ns.route('/<int:perdido_id>')
@perdido_ns.doc(params={'perdido_id': 'O identificador único do perdido'})
class PerdidoDetail(Resource):

    @perdido_ns.doc(responses={200: 'Ok', 404: 'Not Found'})
    @perdido_ns.marshal_with(perdido_output_schema)
    def get(self, perdido_id):
        item = PerdidoService.listar_por_id(perdido_id)
        if not item:
            return {"error": "Item perdido não encontrado."}, 404
        return item, 200