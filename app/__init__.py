from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_login import LoginManager
from gunicorn.config import User
from app.config import Config
<<<<<<< Updated upstream
from app.controller.coupon_controller import coupon_bp
from app.controller.order_controller import order_bp
from app.controller.item_perdido_controller import item_perdido_bp
from app.controller.payment_controller import payment_bp
from app.controller.perdido_controller import perdido_bp
from app.controller.review_controller import review_bp
=======
from app.repository import UserRepository
>>>>>>> Stashed changes

db = SQLAlchemy()
api = Api(title="Marketplace", version="1.0", description="Projeto de Marketplace com Flask")
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    api.init_app(app)
    login_manager.init_app(app)

    #TODO Importar os controllers aqui

<<<<<<< Updated upstream
    app.register_blueprint(coupon_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(item_perdido_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(perdido_bp)
    app.register_blueprint(review_bp)
    
=======
    @login_manager.user_loader
    def load_user(user_id):
        return UserRepository.find_by_id(user_id)

>>>>>>> Stashed changes
    with app.app_context():
        db.create_all()

    return app