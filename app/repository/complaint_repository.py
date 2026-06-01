from app import db
from app.models import ComplaintModel

class ComplaintRepository:
    @staticmethod
    def save(complaint):
        db.session.add(complaint)
        db.session.commit()
        return complaint

    @staticmethod
    def find_by_id(id):
        return ComplaintModel.query.get(id)

    @staticmethod
    def find_by_order_id(order_id):
        return ComplaintModel.query.filter_by(order_id=order_id).all()

    @staticmethod
    def find_by_user_id(user_id):
        return ComplaintModel.query.filter_by(user_id=user_id).all()