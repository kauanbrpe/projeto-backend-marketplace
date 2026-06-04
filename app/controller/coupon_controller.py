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
    'min_order_value': fields.Float(required=True, description='Valor do desconto', example=0.00),
    'max_uses': fields.Integer(required=True, description='Valor do desconto', default=100),
    'is_active': fields.Boolean(required=True, description="Status", default=True)
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
            return CouponService.listar_todos(current_user)
        except PermissionError as e:
            return {'error': str(e)}, 403
        except Exception as e:
            return {'error': "Internal error while retrieving shopping cart."}, 500

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
            return {'error': str(e)}, 401
        except Exception as e:
            return {'error': "Internal error while retrieving shopping cart."}, 500


