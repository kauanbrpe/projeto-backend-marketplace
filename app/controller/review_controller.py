from flask import request
from flask_restx import Namespace, Resource, fields
from flask_login import login_required, current_user
from app.service import ReviewService

review_ns = Namespace('reviews', description='Operações relacionadas às avaliações e comentários de produtos')

review_input_schema = review_ns.model('ReviewInput', {
    'product_id': fields.Integer(required=True, description='ID do produto avaliado', example=1),
    'rating': fields.Integer(required=True, description='Nota de 1 a 5 estrelas', example=5),
    'title': fields.String(required=False, description='Título curto do comentário', example='Excelente custo-benefício!'),
    'comment': fields.String(required=False, description='Texto detalhado sobre a experiência', example='O produto chegou super rápido.')
})

review_update_schema = review_ns.model('ReviewUpdateInput', {
    'rating': fields.Integer(required=False, description='Nova nota de 1 a 5'),
    'title': fields.String(required=False, description='Novo título'),
    'comment': fields.String(required=False, description='Novo comentário')
})

review_output_schema = review_ns.model('ReviewOutput', {
    'id': fields.Integer(description='ID único da avaliação'),
    'rating': fields.Integer(description='Nota dada pelo cliente'),
    'title': fields.String(description='Título do comentário'),
    'comment': fields.String(description='Texto do comentário'),
    'user_id': fields.Integer(description='ID do usuário que avaliou'),
    'product_id': fields.Integer(description='ID do produto avaliado')
})

@review_ns.route('/')
class ReviewCreate(Resource):

    @review_ns.expect(review_input_schema)
    @review_ns.doc(responses={201: 'Created', 400: 'Invalid', 401: 'Unauthorized'})
    @login_required
    def post(self):
        data = request.json

        if not data or 'product_id' not in data or 'rating' not in data:
            return {"error": "Dados incompletos. O ID do produto e a nota são obrigatórios."}, 400

        nova_review = ReviewService.criar_avaliacao(
            user_id=current_user.id,
            product_id=data['product_id'],
            nota=data['rating'],
            titulo=data.get('title'),
            comentario=data.get('comment')
        )

        if nova_review is False:
            return {"error": "Erro de validação: A nota deve estar entre 1 e 5 estrelas."}, 400

        return nova_review.to_dict(), 201

@review_ns.route('/<int:review_id>')
@review_ns.doc(params={'review_id': 'O identificador único da avaliação'})
class ReviewDetail(Resource):

    @review_ns.expect(review_update_schema)
    @review_ns.doc(responses={200: 'Ok', 400: 'Invalid', 401: 'Unauthorized', 403: 'Forbidden', 404: 'Not Found'})
    @login_required
    def put(self, review_id):
        data = request.json
        if not data:
            return {"error": "Nenhum dado enviado para atualização."}, 400

        try:
            updated = ReviewService.atualizar_avaliacao(review_id, data, current_user)
            return updated.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 404
        except PermissionError as e:
            return {"error": str(e)}, 403
        except Exception as e:
            return {"error": "Erro interno ao atualizar a avaliação."}, 500

    @review_ns.doc(responses={200: 'Ok', 401: 'Unauthorized', 403: 'Forbidden', 404: 'Not Found'})
    @login_required
    def delete(self, review_id):
        try:
            ReviewService.deletar_avaliacao(review_id, current_user)
            return {"message": "Avaliação excluída com sucesso."}, 200
        except ValueError as e:
            return {"error": str(e)}, 404
        except PermissionError as e:
            return {"error": str(e)}, 403
        except Exception as e:
            return {"error": "Erro interno ao excluir a avaliação."}, 500

@review_ns.route('/product/<int:product_id>')
@review_ns.doc(params={'product_id': 'O identificador exclusivo do produto'})
class ReviewProductList(Resource):

    @review_ns.doc(responses={200: 'Ok'})
    @review_ns.marshal_list_with(review_output_schema)
    def get(self, product_id):
        try:
            return ReviewService.listar_por_produto(product_id), 200
        except Exception as e:
            return {"error": "Erro interno ao buscar as avaliações do produto."}, 500

@review_ns.route('/user/<int:user_id>')
@review_ns.doc(params={'user_id': 'O identificador único do usuário'})
class ReviewUserList(Resource):

    @review_ns.doc(responses={200: 'Ok'})
    @review_ns.marshal_list_with(review_output_schema)
    def get(self, user_id):
        try:
            return ReviewService.listar_por_user_id(user_id), 200
        except Exception as e:
            return {"error": "Erro interno ao buscar as avaliações do usuário."}, 500
