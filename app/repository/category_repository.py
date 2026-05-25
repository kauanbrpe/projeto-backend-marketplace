from app import db
from app.models import CategoryModel

class CategoryRepository:
    @staticmethod
    def save(category):
        db.session.add(category)
        db.session.commit()
        return category

    @staticmethod
    def find_by_id(category_id):
        return CategoryModel.query.get(category_id)