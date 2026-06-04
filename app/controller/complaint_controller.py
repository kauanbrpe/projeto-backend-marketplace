from flask import request
from flask_restx import Namespace, Resource, fields
from flask_login import login_required, current_user
from app.service import ComplaintService

complaint_ns = Namespace("complaints", description="Operações relacionadas para as reclamações dos usuários")

complaint_schema = complaint_ns.model("ComplaintItem", {
    'description': fields.String(required=True, description="Descrição da Reclamação")
})

@complaint_ns.route('/')
class ComplaintController(Resource):

    @complaint_ns.expect(complaint_schema)
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
            return new_complaint, 200

        except ValueError as e:
            return {'message': str(e)}, 400
        except PermissionError as e:
            return {'message': str(e)}, 401
        except Exception as e:
            return {'error': "Internal error processing the request."}, 500
