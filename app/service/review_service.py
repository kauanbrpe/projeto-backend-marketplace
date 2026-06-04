from app.models.review_model import ReviewModel
from app.repository import ReviewRepository

class ReviewService:
    @staticmethod
    def listar_por_produto(product_id):
        return ReviewRepository.find_by_id(product_id)

    @staticmethod
    def listar_por_user_id(user_id):
        return ReviewRepository.find_by_user_id(user_id)

    @staticmethod
    def criar_avaliacao(user_id, product_id, nota, titulo, comentario):
        
        if nota < 1:
            return False
        if nota > 5:
            return False
            
        nova_review = ReviewModel(
            user_id=user_id,
            product_id=product_id,
            rating=int(nota),
            title=titulo,       
            comment=comentario
        )

        return ReviewRepository.save(nova_review)