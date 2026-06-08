from flask import request
from flask_restx import Namespace, Resource, fields
from flask_login import login_required, current_user
from app.service import ComplaintService

complaint_ns = Namespace("complaints", description="Operações relacionadas para as reclamações dos usuários")

complaint_input_schema = complaint_ns.model("ComplaintInput", {
    'order_id': fields.Integer(required=True, description="ID do pedido relacionado"),
    'description': fields.String(required=True, description="Descrição da Reclamação")
})

complaint_update_schema = complaint_ns.model("ComplaintUpdateInput", {
    'description': fields.String(required=False, description="Nova descrição"),
    'status': fields.String(required=False, description="Novo status (apenas admin)", example="Em análise")
})

complaint_output_schema = complaint_ns.model("ComplaintOutput", {
    'id': fields.Integer(description='ID único da reclamação'),
    'order_id': fields.Integer(description='ID do pedido'),
    'user_id': fields.Integer(description='ID do usuário'),
    'description': fields.String(description='Descrição'),
    'status': fields.String(description='Status da reclamação'),
    'created_at': fields.String(description='Data de criação')
})

@complaint_ns.route('/')
class ComplaintList(Resource):

    @complaint_ns.doc(responses={200: 'Ok', 401: 'Unauthorized', 403: 'Forbidden'})
    @complaint_ns.marshal_list_with(complaint_output_schema)
    @login_required
    def get(self):
        try:
            if current_user.is_admin:
                reclamacoes = ComplaintService.listar_todas(current_user)
            else:
                reclamacoes = ComplaintService.listar_por_usuario(current_user.id)
            return reclamacoes, 200
        except PermissionError as e:
            return {'error': str(e)}, 403
        except Exception as e:
            return {'error': "Erro interno ao listar reclamações."}, 500

    @complaint_ns.expect(complaint_input_schema)
    @complaint_ns.doc(responses={201: 'Created', 400: 'Validation Error', 401: 'Unauthorized'})
    @login_required
    def post(self):
        data = request.json

        try:
            new_complaint = ComplaintService.abrir_reclamacao(
                user=current_user,
                order_id=data['order_id'],
                descricao=data['description'],
            )

            if new_complaint is None:
                return {'error': "Pedido não encontrado."}, 404

            if new_complaint is False:
                return {'error': "Só é possível abrir reclamações em pedidos com status 'Entregue'."}, 400

            return new_complaint.to_dict(), 201

        except ValueError as e:
            return {'error': str(e)}, 400
        except PermissionError as e:
            return {'error': str(e)}, 401
        except Exception as e:
            return {'error': "Erro interno ao processar a reclamação."}, 500

@complaint_ns.route('/<int:complaint_id>')
@complaint_ns.doc(params={'complaint_id': 'O identificador único da reclamação'})
class ComplaintDetail(Resource):

    @complaint_ns.doc(responses={200: 'Ok', 401: 'Unauthorized', 403: 'Forbidden', 404: 'Not Found'})
    @complaint_ns.marshal_with(complaint_output_schema)
    @login_required
    def get(self, complaint_id):
        reclamacao = ComplaintService.listar_por_id(complaint_id)
        if not reclamacao:
            return {"error": "Reclamação não encontrada."}, 404

        if reclamacao.user_id != current_user.id and not current_user.is_admin:
            return {"error": "Acesso negado: Esta reclamação pertence a outro usuário."}, 403

        return reclamacao, 200

    @complaint_ns.expect(complaint_update_schema)
    @complaint_ns.doc(responses={200: 'Ok', 400: 'Invalid', 401: 'Unauthorized', 403: 'Forbidden', 404: 'Not Found'})
    @login_required
    def put(self, complaint_id):
        data = request.json
        if not data:
            return {"error": "Nenhum dado enviado para atualização."}, 400

        try:
            updated = ComplaintService.atualizar_reclamacao(complaint_id, data, current_user)
            return updated.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 404
        except PermissionError as e:
            return {"error": str(e)}, 403
        except Exception as e:
            return {"error": "Erro interno ao atualizar a reclamação."}, 500

    @complaint_ns.doc(responses={200: 'Ok', 401: 'Unauthorized', 403: 'Forbidden', 404: 'Not Found'})
    @login_required
    def delete(self, complaint_id):
        try:
            ComplaintService.deletar_reclamacao(complaint_id, current_user)
            return {"message": "Reclamação excluída com sucesso."}, 200
        except ValueError as e:
            return {"error": str(e)}, 404
        except PermissionError as e:
            return {"error": str(e)}, 403
        except Exception as e:
            return {"error": "Erro interno ao excluir a reclamação."}, 500
