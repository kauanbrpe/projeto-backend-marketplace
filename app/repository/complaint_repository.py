from app import db
from app.models import ComplaintModel

class ComplaintRepository:
    @staticmethod
    def save(complaint):
        db.session.add(complaint)
        db.session.commit()
        return complaint

    @staticmethod
    def find_by_id(complaint_id):
        return db.session.get(ComplaintModel, complaint_id)

    @staticmethod
    def find_by_order_id(order_id):
        return ComplaintModel.query.filter_by(order_id=order_id).all()

    @staticmethod
    def find_by_user_id(user_id):
        return ComplaintModel.query.filter_by(user_id=user_id).all()

    @staticmethod
    def find_all():
        return ComplaintModel.query.all()

    @staticmethod
    def update(complaint):
        db.session.add(complaint)
        db.session.commit()
        return complaint

    @staticmethod
    def delete(complaint):
        db.session.delete(complaint)
        db.session.commit()
        return True
