from app import db
from app.models import ReviewModel

class ReviewRepository:
    @staticmethod
    def save(review):
        db.session.add(review)
        db.session.commit()
        return review

    @staticmethod
    def find_by_id(review_id):
        return ReviewModel.query.get(review_id)

    @staticmethod
    def find_by_product_id(product_id):
        return ReviewModel.query.filter_by(product_id=product_id).all()

    @staticmethod
    def find_by_user_id(user_id):
        return ReviewModel.query.filter_by(user_id=user_id).all()

    @staticmethod
    def update(review):
        db.session.add(review)
        db.session.commit()
        return review

    @staticmethod
    def delete(review):
        db.session.delete(review)
        db.session.commit()
        return True
