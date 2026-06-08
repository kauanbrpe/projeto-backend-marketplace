from app.models.review_model import ReviewModel
from app.repository import ReviewRepository

class ReviewService:
    @staticmethod
    def listar_por_produto(product_id):
        return ReviewRepository.find_by_product_id(product_id)

    @staticmethod
    def listar_por_user_id(user_id):
        return ReviewRepository.find_by_user_id(user_id)

    @staticmethod
    def listar_por_id(review_id):
        return ReviewRepository.find_by_id(review_id)

    @staticmethod
    def criar_avaliacao(user_id, product_id, nota, titulo, comentario):
        if nota < 1 or nota > 5:
            return False

        nova_review = ReviewModel(
            user_id=user_id,
            product_id=product_id,
            rating=int(nota),
            title=titulo,
            comment=comentario
        )

        return ReviewRepository.save(nova_review)

    @staticmethod
    def atualizar_avaliacao(review_id, dados, current_user):
        review = ReviewRepository.find_by_id(review_id)
        if not review:
            raise ValueError("Erro: Avaliação não encontrada!")

        if review.user_id != current_user.id and not current_user.is_admin:
            raise PermissionError("Acesso negado: Você não pode editar a avaliação de outro usuário.")

        if 'rating' in dados:
            if dados['rating'] < 1 or dados['rating'] > 5:
                raise ValueError("Erro: A nota deve estar entre 1 e 5.")
            review.rating = int(dados['rating'])
        if 'title' in dados:
            review.title = dados['title']
        if 'comment' in dados:
            review.comment = dados['comment']

        return ReviewRepository.update(review)

    @staticmethod
    def deletar_avaliacao(review_id, current_user):
        review = ReviewRepository.find_by_id(review_id)
        if not review:
            raise ValueError("Erro: Avaliação não encontrada!")

        if review.user_id != current_user.id and not current_user.is_admin:
            raise PermissionError("Acesso negado: Você não pode excluir a avaliação de outro usuário.")

        ReviewRepository.delete(review)
        return True
