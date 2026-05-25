from app import db
from app.models import UserModel

class UserRepository:
    @staticmethod
    def save(user):
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def find_by_id(user_id):
        return UserModel.query.get(user_id)

    @staticmethod
    def find_by_email(email):
        return UserModel.query.filter_by(email=email).first()