from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_login import LoginManager
from app.config import Config
from app.controller.coupon_controller import coupon_bp
from app.controller.order_controller import order_bp
from app.controller.item_perdido_controller import item_perdido_bp
from app.controller.payment_controller import payment_bp
from app.controller.perdido_controller import perdido_bp
from app.controller.review_controller import review_bp
from app.controller.cart_controller import cart_bp
from app.controller.category_controller import category_bp
from app.controller.complaint_controller import complaint_bp
from app.controller.product_controller import product_bp
from app.controller.user_controller import user_bp
from app.repository import UserRepository

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

    app.register_blueprint(coupon_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(item_perdido_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(perdido_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(complaint_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return UserRepository.find_by_id(user_id)

    with app.app_context():
        db.create_all()

    return app