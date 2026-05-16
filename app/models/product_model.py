from app import db

class ProductModel(db.Model):
    __tablename__ = 'product'

    id = db.Cloumn(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": float(self.price)}
