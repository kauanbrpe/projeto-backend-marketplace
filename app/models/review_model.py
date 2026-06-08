from app import db
from datetime import datetime

class ReviewModel(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=True)
    comment = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "rating": self.rating,
            "title": self.title,
            "comment": self.comment,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "created_at": self.created_at.isoformat()
        }