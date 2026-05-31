from app.models.review import Review
from app import db

class ReviewRepository:
    @staticmethod
    def salvar(review):
        db.session.add(review)
        db.session.commit()
        return review

    @staticmethod
    def listar_por_produto(produto_id):
        return Review.query.filter_by(product_id=produto_id).all()