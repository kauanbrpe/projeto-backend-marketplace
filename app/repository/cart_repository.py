from app import db
from app.models.cart_model import CartModel, cart_items

class CartRepository:
    @staticmethod
    def save(cart):
        db.session.add(cart)
        db.session.commit()
        return cart

    @staticmethod
    def find_by_user_id(user_id):
        return CartModel.query.filter_by(user_id=user_id).first()

    @staticmethod
    def add_item(cart_id, product_id, quantity=1):
        stmt = cart_items.insert().values(cart_id=cart_id, product_id=product_id, quantity=quantity)
        db.session.execute(stmt)
        db.session.commit()

    @staticmethod
    def update_item_quantity(cart_id, product_id, quantity):
        stmt = cart_items.update().where(
            (cart_items.c.cart_id == cart_id) &
            (cart_items.c.product_id == product_id)
        ).values(quantity=quantity)
        db.session.execute(stmt)
        db.session.commit()

    @staticmethod
    def remove_item(cart_id, product_id):
        stmt = cart_items.delete().where(
            (cart_items.c.cart_id == cart_id) &
            (cart_items.c.product_id == product_id)
        )
        db.session.execute(stmt)
        db.session.commit()

    @staticmethod
    def get_item_quantity(cart_id, product_id):
        stmt = db.select(cart_items.c.quantity).where(
            (cart_items.c.cart_id == cart_id) &
            (cart_items.c.product_id == product_id)
        )
        result = db.session.execute(stmt)
        return result