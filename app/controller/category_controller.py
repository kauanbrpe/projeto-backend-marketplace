from flask import request
from flask_restx import Namespace, Resource, fields
from flask_login import login_required, current_user
from app.service import CategoryService

category_ns = Namespace("categories", description="Operações relacionadas as categorias de Produtos")

category_input_schema = category_ns.model('CategoryInput', {
    'name': fields.String(required=True, description='Nome da categoria'),
})

category_update_schema = category_ns.model('CategoryUpdateInput', {
    'name': fields.String(required=True, description='Novo nome da categoria'),
})

category_output_schema = category_ns.model('CategoryOutput', {
    'id': fields.Integer(description='ID único da categoria'),
    'name': fields.String(description='Nome da categoria'),
})

@category_ns.route('/')
class CategoryList(Resource):

    @category_ns.doc(responses={200: 'Ok'})
    @category_ns.marshal_list_with(category_output_schema)
    def get(self):
        try:
            return CategoryService.listar_todas(), 200
        except Exception as e:
            return {'error': "Erro interno ao listar categorias."}, 500

    @category_ns.expect(category_input_schema)
    @category_ns.doc(responses={201: 'Created', 400: 'Validation Error', 401: 'Unauthorized'})
    @login_required
    def post(self):
        data = request.json

        try:
            new_category = CategoryService.criar_categoria(data)
            return new_category.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': "Erro interno ao criar a categoria."}, 500

@category_ns.route('/<int:category_id>')
@category_ns.doc(params={'category_id': 'O identificador único da categoria'})
class CategoryDetail(Resource):

    @category_ns.doc(responses={200: 'Ok', 404: 'Not Found'})
    @category_ns.marshal_with(category_output_schema)
    def get(self, category_id):
        categoria = CategoryService.listar_por_id(category_id)
        if not categoria:
            return {"error": "Categoria não encontrada."}, 404
        return categoria, 200

    @category_ns.expect(category_update_schema)
    @category_ns.doc(responses={200: 'Ok', 400: 'Invalid', 401: 'Unauthorized', 403: 'Forbidden', 404: 'Not Found'})
    @login_required
    def put(self, category_id):
        data = request.json
        if not data:
            return {"error": "Nenhum dado enviado para atualização."}, 400

        try:
            updated = CategoryService.atualizar_categoria(category_id, data, current_user)
            return updated.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 404
        except PermissionError as e:
            return {"error": str(e)}, 403
        except Exception as e:
            return {"error": "Erro interno ao atualizar a categoria."}, 500

    @category_ns.doc(responses={200: 'Ok', 401: 'Unauthorized', 403: 'Forbidden', 404: 'Not Found'})
    @login_required
    def delete(self, category_id):
        try:
            CategoryService.deletar_categoria(category_id, current_user)
            return {"message": "Categoria excluída com sucesso."}, 200
        except ValueError as e:
            return {"error": str(e)}, 404
        except PermissionError as e:
            return {"error": str(e)}, 403
        except Exception as e:
            return {"error": "Erro interno ao excluir a categoria."}, 500
