from flask import request
from flask_restx import Namespace, Resource, fields
from flask_login import login_required, current_user
from app.service import CouponService

coupon_ns = Namespace('coupons', description="Operações relacionadas ao coupons")

coupon_input_schema = coupon_ns.model('CouponInput', {
    'code': fields.String(required=True, description='Código do Cupom'),
    'discount_type': fields.String(required=True, description='fixed ou percentage', example='percentage'),
    'discount_value': fields.Float(required=True, description='Valor do desconto', example=20.00),
    'expiration_date': fields.String(required=True, description='Data de expiração (AAAA-MM-DD)', example='2026-12-31'),
    'min_order_value': fields.Float(required=False, description='Valor mínimo do pedido', example=0.00),
    'max_uses': fields.Integer(required=False, description='Limite total de usos', default=100),
    'is_active': fields.Boolean(required=False, description="Status", default=True)
})

coupon_output_schema = coupon_ns.model('CouponOutput', {
    'id': fields.Integer(description='Identificador único do cupom'),
    'code': fields.String(description='Código do cupom'),
    'discount_type': fields.String(description='Tipo de desconto'),
    'discount_value': fields.Float(description='Valor do desconto'),
    'min_order_value': fields.Float(description='Valor mínimo exigido'),
    'expiration_date': fields.String(description='Data de validade'),
    'max_uses': fields.Integer(description='Limite total de usos'),
    'used_count': fields.Integer(description='Quantidade de vezes utilizado'),
    'is_active': fields.Boolean(description='Se o cupom está ativo')
})

@coupon_ns.route('/')
class CouponList(Resource):

    @coupon_ns.doc(responses={200: 'Ok', 401: 'Unauthorized', 403: "Permission denied"})
    @coupon_ns.marshal_list_with(coupon_output_schema)
    @login_required
    def get(self):
        if not current_user.is_admin:
            return {'error': 'Permission denied'}, 403

        try:
            return CouponService.listar_todos(current_user), 200
        except PermissionError as e:
            return {'error': str(e)}, 403
        except Exception as e:
            return {'error': "Erro interno ao listar cupons."}, 500

    @coupon_ns.expect(coupon_input_schema)
    @coupon_ns.doc(responses={201: 'Created', 401: 'Unauthorized', 403: "Permission denied"})
    @login_required
    def post(self):
        if not current_user.is_admin:
            return {'error': 'Permission denied'}, 403

        data = request.json
        try:
            new_coupon = CouponService.criar_cupom(data, current_user)
            return new_coupon.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except PermissionError as e:
            return {'error': str(e)}, 403
        except Exception as e:
            return {'error': "Erro interno ao criar cupom."}, 500

@coupon_ns.route('/<int:coupon_id>')
@coupon_ns.doc(params={'coupon_id': 'O identificador único do cupom'})
class CouponDetail(Resource):

    @coupon_ns.doc(responses={200: 'Ok', 401: 'Unauthorized', 403: 'Forbidden', 404: 'Not Found'})
    @login_required
    def delete(self, coupon_id):
        try:
            CouponService.deletar_cupom(coupon_id, current_user)
            return {"message": "Cupom excluído com sucesso."}, 200
        except ValueError as e:
            return {"error": str(e)}, 404
        except PermissionError as e:
            return {"error": str(e)}, 403
        except Exception as e:
            return {"error": "Erro interno ao excluir o cupom."}, 500
