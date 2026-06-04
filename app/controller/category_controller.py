from flask import request
from flask_restx import Namespace, Resource, fields
from flask_login import login_required
from app.service import CategoryService

category_ns = Namespace("categories", description="Operações relacionadas as categorias de Produtos")

category_schema = category_ns.model('CategoryItem', {
    'name': fields.String(required=True, description='Nome do produto'),
})

@category_ns.route('/')
class CategoryController(Resource):

    @category_ns.expect(category_schema)
    @category_ns.doc(responses={201: 'Created', 400: 'Validation Error', 401: "Unauthorized"})
    @login_required
    def post(self):
        data = request.json

        try:
            new_category = CategoryService.criar_categoria(
                data['name'],
            )
            return new_category.to_dict(), 201

        except ValueError as e:
            return {'message': str(e)}, 400
        except PermissionError as e:
            return {'message': str(e)}, 401
        except Exception as e:
            return {'error': "Internal error processing the request."}, 500
