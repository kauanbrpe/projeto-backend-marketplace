from app import db
from flask_login import UserMixin

class UserModel(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email= db.Column(db.String(120), unique=True, nullable=False)
    endereco = db.Column(db.String(80), nullable=False)

    password_hash = db.Column(db.String(128), nullable=False)

    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, name, email, endereco, password_hash, is_admin=False):
        self.name = name
        self.email = email
        self.endereco = endereco
        self.password_hash = password_hash
        self.is_admin = is_admin

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email, "endereco": self.endereco, "is_admin": self.is_admin}