from app.models.perdido import Perdido
from app import db

class PerdidoRepository:
    @staticmethod
    def listar_todos():
        return Perdido.query.all()

    @staticmethod
    def salvar(perdido):
        db.session.add(perdido)
        db.session.commit()
        return perdido