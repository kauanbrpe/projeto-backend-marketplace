from flask import request
from flask_restx import Namespace, Resource, fields
from flask_login import login_required, current_user
from app.service import ReviewService

review_ns = Namespace('reviews', description='Operações relacionadas às avaliações e comentários de produtos')

review_input_schema = review_ns.model('ReviewInput', {
    'product_id': fields.Integer(required=True, description='ID do produto que está sendo avaliado', example=1),
    'rating': fields.Integer(required=True, description='Nota de 1 a 5 estrelas', example=5),
    'title': fields.String(required=False, description='Título curto do comentário', example='Excelente custo-benefício!'),
    'comment': fields.String(required=False, description='Texto detalhado sobre a experiência com o produto', example='O produto chegou super rápido e funciona perfeitamente.')
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

        if not data or 'product_id' not in data or 'nota' not in data:
            return {"error": "Dados incompletos. O ID do produto e a nota são obrigatórios."}, 400

        nova_review = ReviewService.criar_avaliacao(
            user_id=current_user.id,  # Injeta o ID de forma segura direto do Flask-Login
            product_id=data['product_id'],
            nota=data['rating'],
            titulo=data.get('title'),
            comentario=data.get('comment')
        )

        if nova_review is False:
            return {
                "error": "Erro de validação: A nota da avaliação deve estar obrigatoriamente entre 1 e 5 estrelas."}, 400

        return nova_review.to_dict(), 201

@review_ns.route('/product/<int:product_id>')
@review_ns.doc(params={'product_id': 'O identificador exclusivo do produto'})
class ReviewProductList(Resource):

    @review_ns.doc(resposes={200: 'Ok'})
    @review_ns.marshal_list_with(review_output_schema)
    def get(self, product_id):
        try:
            avaliacoes = ReviewService.listar_por_produto(product_id)

            return avaliacoes, 200

        except Exception as e:
            return {"error": "Erro interno ao buscar as avaliações do produto."}, 500

@review_ns.route('/user/<int:user_id>')
@review_ns.doc(params={'user_id': 'O identificador único do Usuário'})
class ReviewUserList(Resource):

    @review_ns.doc(resposes={200: 'Ok'})
    @review_ns.marshal_list_with(review_output_schema)
    def get(self, user_id):
        try:
            avaliacoes = ReviewService.listar_por_user_id(user_id)

            return avaliacoes, 200

        except Exception as e:
            return {"error": "Erro interno ao buscar as avaliações do produto."}, 500