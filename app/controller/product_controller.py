from flask import request
from flask_restx import Namespace, Resource, fields
from flask_login import login_required, current_user
from app.service import ProductService

product_ns = Namespace('products', description='Operações relacionadas ao catálogo de produtos do marketplace')

product_input_schema = product_ns.model('ProductInput', {
    'name': fields.String(required=True, description='Nome do produto', example='Monitor Gamer 24" 144Hz'),
    'price': fields.Float(required=True, description='Preço unitário de venda', example=899.90),
    'stock': fields.Integer(required=True, description='Quantidade inicial em estoque', example=15),
    'category_id': fields.Integer(required=True, description='ID da categoria associada', example=1)
})

product_output_schema = product_ns.model('ProductOutput', {
    'id': fields.Integer(description='ID único do produto'),
    'name': fields.String(description='Nome do produto'),
    'price': fields.Float(description='Preço do produto'),
    'stock': fields.Integer(description='Quantidade em estoque'),
    'category_id': fields.Integer(description='ID da categoria'),
    'seller_id': fields.Integer(description='ID do usuário vendedor')
})

@product_ns.route('/')
class ProductList(Resource):

    @product_ns.doc(resposes={200: 'Ok'})
    @product_ns.marshal_with(product_output_schema)
    def get(self):
        try:
            return ProductService.listar_produtos(), 200
        except Exception as e:
            return {"error": "Erro interno ao listar os produtos do catálogo."}, 500

    @product_ns.expect(product_input_schema)
    @product_ns.doc(responses={201: 'Created', 400: 'Invalid', 401: 'Unauthorized'})
    @login_required
    def post(self):
        data = request.json

        if not data or 'name' not in data or 'category_id' not in data:
            return {"error": "Dados incompletos. Nome e Categoria são obrigatórios."}, 400

        try:
            data['seller_id'] = current_user.id

            new_product = ProductService.criar_produto(data)
            return new_product.to_dict(), 201

        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": "Erro interno ao processar o cadastro do produto."}, 500

@product_ns.route('/<int:product_id>')
@product_ns.doc(params={'product_id': 'O identificador único do produto'})
class ProductDetail(Resource):

    @product_ns.doc(responses={200: 'Ok', 404: 'Not Found'})
    @product_ns.marshal_with(product_output_schema)
    def get(self, product_id):
        try:
            product = ProductService.listar_produto_por_id(product_id)
            return product, 200
        except ValueError as e:
            return {"error": str(e)}, 404
        except Exception as e:
            return {"error": "Erro interno ao processar a busca do produto."}, 500

@product_ns.route('/user/<int:user_id>')
class UserProducts(Resource):

    @product_ns.doc(responses={200: 'Ok', 404: 'Not Found'})
    @product_ns.marshal_with(product_output_schema)
    def get(self, user_id):
        try:
            product = ProductService.listar_produto_por_user_id(user_id)
            return product, 200
        except ValueError as e:
            return {"error": str(e)}, 404
        except Exception as e:
            return {"error": "Erro interno ao processar a busca do produto."}, 500