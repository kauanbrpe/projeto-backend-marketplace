from app import db
from app.models.review_model import ReviewModel

class ReviewService:
    @staticmethod
    def listar_por_produto(product_id):
        return ReviewModel.query.filter_by(product_id=product_id).all()

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
        db.session.add(nova_review)
        db.session.commit()
        return nova_review