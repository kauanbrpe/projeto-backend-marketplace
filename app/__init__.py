from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from app.config import Config

db = SQLAlchemy()
api = Api(title="Marketplace", version="1.0", description="Projeto de Marketplace com Flask")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    api.init_app(app)

    #TODO Importar os controllers aqui

    with app.app_context():
        db.create_all()

    return app