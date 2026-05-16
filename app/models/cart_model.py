from app import db

cart_items = db.Table('cart_items',
    db.Column('cart_id', db.Integer, db.ForeignKey('carts.id', ondelete='CASCADE'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('quantity', db.Integer, default=1, nullable=False)
)

class CartModel(db.Model):
    __tablename__ = "carts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    products = db.relationship('ProductModel', secondary=cart_items, lazy='subquery')

    def to_dict(self):
        return {"id": self.id, "user_id": self.user_id, "products": [product.to_dict() for product in self.products]}