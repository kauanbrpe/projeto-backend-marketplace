from flask import request
from flask_restx import Namespace, Resource, fields
from flask_login import login_required, current_user
from app.service import CartService

cart_ns = Namespace('carts', description='Operações relacionadas ao carrinho de compras')

cart_item_schema = cart_ns.model('CartItemInput', {
    'product_id': fields.Integer(required=True, description='ID do produto'),
    'quantity': fields.Integer(required=True, description='Quantidade do produto', default=1)
})

cart_update_schema = cart_ns.model('CartUpdateInput', {
    'product_id': fields.Integer(required=True, description='ID do produto'),
    'quantity': fields.Integer(required=True, description='Nova quantidade desejada')
})

@cart_ns.route('/')
class CartController(Resource):

    @cart_ns.doc(responses={200: 'Ok', 401: 'Unauthorized'})
    @login_required
    def get(self):
        try:
            cart = CartService.get_or_create_cart(current_user)
            return cart, 200
        except PermissionError as e:
            return {'error': str(e)}, 401
        except Exception as e:
            return {'error': "Erro interno ao recuperar o carrinho."}, 500

    @cart_ns.expect(cart_item_schema)
    @cart_ns.doc(responses={200: 'Ok', 400: 'Validation/Inventory Error', 401: 'Unauthorized'})
    @login_required
    def post(self):
        data = request.json

        if not data or 'product_id' not in data or 'quantity' not in data:
            return {'error': 'Missing product or quantity'}, 400

        try:
            updated_cart = CartService.add_product(
                product_id=data['product_id'],
                quantity=data['quantity'],
                current_user=current_user
            )
            return updated_cart, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except PermissionError as e:
            return {'error': str(e)}, 401

    @cart_ns.expect(cart_update_schema)
    @cart_ns.doc(responses={200: 'Ok', 400: 'Invalid', 401: 'Unauthorized'})
    @login_required
    def put(self):
        data = request.json

        if not data or 'product_id' not in data or 'quantity' not in data:
            return {'error': 'Missing product_id or quantity'}, 400

        try:
            updated_cart = CartService.update_product_quantity(
                product_id=data['product_id'],
                quantity=data['quantity'],
                current_user=current_user
            )
            return updated_cart, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except PermissionError as e:
            return {'error': str(e)}, 401
        except Exception as e:
            return {'error': "Erro interno ao atualizar o carrinho."}, 500

    @cart_ns.expect(cart_item_schema)
    @cart_ns.doc(responses={200: 'Ok', 400: 'Validation/Inventory Error', 401: 'Unauthorized'})
    @login_required
    def delete(self):
        data = request.json

        if not data or 'product_id' not in data:
            return {'error': 'Missing product_id'}, 400

        try:
            removed_cart = CartService.remove_product(
                product_id=data['product_id'],
                current_user=current_user
            )
            return removed_cart, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except PermissionError as e:
            return {'error': str(e)}, 401

@cart_ns.route('/apply-coupon')
class CartApplyCoupon(Resource):

    coupon_req_schema = cart_ns.model('ApplyCouponInput', {
        'code': fields.String(required=True, description='Código do cupom de desconto', example='CUPOM20')
    })

    @cart_ns.expect(coupon_req_schema)
    @cart_ns.doc(responses={200: 'Ok', 400: 'Invalid', 401: 'Unauthorized'})
    @login_required
    def post(self):
        data = request.json

        if not data or 'code' not in data:
            return {'error': 'Missing code'}, 400

        try:
            result = CartService.add_coupon_cart(
                code_coupon=data['code'],
                current_user=current_user
            )
            return result, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except PermissionError as e:
            return {'error': str(e)}, 401