from app import db

class ProductModel(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    
    stock = db.Column(db.Integer, nullable=False, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id, 
            "name": self.name, 
            "price": float(self.price), 
            "stock": self.stock, 
            "category_id": self.category_id, 
            "seller_id": self.seller_id}

    
    
    
    
