from app import db
from app.models import PerdidoModel

class PerdidoRepository:
    @staticmethod
    def save(perdido):
        db.session.add(perdido)
        db.session.commit()
        return perdido

    @staticmethod
    def find_by_id(perdido_id):
        return PerdidoModel.query.get(perdido_id)

    @staticmethod
    def find_by_user_id(user_id):
        return PerdidoModel.query.filter_by(user_id=user_id).first()