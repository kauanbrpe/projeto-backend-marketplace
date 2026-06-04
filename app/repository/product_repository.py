from app import db
from app.models import ProductModel

class ProductRepository:
    @staticmethod
    def save(product):
        db.session.add(product)
        db.session.commit()
        return product

    @staticmethod
    def get_all():
        return ProductModel.query.all()

    @staticmethod
    def find_by_id(product_id):
        return ProductModel.query.get(product_id)

    @staticmethod
    def find_by_user_id(user_id):
        return ProductModel.query.get(user_id)