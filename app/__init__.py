from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_login import LoginManager
from app.config import Config

db = SQLAlchemy()
api = Api(title="Marketplace", version="1.0", description="Projeto de Marketplace com Flask")
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    api.init_app(app)
    login_manager.init_app(app)

    #TODO Importar o UserRepository aqui
    from app.repository import UserRepository

    @login_manager.user_loader
    def load_user(user_id):
        return UserRepository.find_by_id(user_id)

    #TODO Importar os controllers aqui
    from app.controller.cart_controller import cart_ns
    from app.controller.category_controller import category_ns
    from app.controller.complaint_controller import complaint_ns
    from app.controller.coupon_controller import coupon_ns
    from app.controller.item_perdido_controller import item_perdido_ns
    from app.controller.order_controller import order_ns
    from app.controller.payment_controller import payment_ns
    from app.controller.perdido_controller import perdido_ns
    from app.controller.product_controller import product_ns
    from app.controller.review_controller import review_ns
    from app.controller.user_controller import user_ns

    #TODO Puxar o Namespace dos controllers aqui
    api.add_namespace(cart_ns, path='/carts')
    api.add_namespace(category_ns, path='/categories')
    api.add_namespace(complaint_ns, path='/complaints')
    api.add_namespace(coupon_ns, path='/coupons')
    api.add_namespace(item_perdido_ns, path='/itensperdidos')
    api.add_namespace(order_ns, path='/orders')
    api.add_namespace(payment_ns, path='/payments')
    api.add_namespace(perdido_ns, path='/perdidos')
    api.add_namespace(product_ns, path='/products')
    api.add_namespace(review_ns, path='/reviews')
    api.add_namespace(user_ns, path='/users')

    with app.app_context():
        db.create_all()

    return app