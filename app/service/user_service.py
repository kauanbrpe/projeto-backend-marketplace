from app.models import UserModel
from app.repository import UserRepository
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user

class UserService:
    @staticmethod
    def user_registration(data):
        if not data.get("name") or not data.get("email") or not data.get("password"):
            raise ValueError("Error: Name, email, and password required.")

        existing_user = UserRepository.find_by_email(data['email'])
        if existing_user:
            raise ValueError("Error: Email already exists.")

        new_user = UserModel(
            name=data['name'],
            email=data['email'],
            endereco=data['endereco'],
            password_hash=data['password'],
            is_admin = data.get('is_admin', False)
        )

        return UserRepository.save(new_user)

    @staticmethod
    def log_in(email, password):
        if not email or not password:
            raise ValueError("Error: Email and senha required.")

        user = UserRepository.find_by_email(email)

        if not user or not check_password_hash(user.password_hash, password):
            raise ValueError("Error: Incorrect email or password")

        login_user(user)
        return user

    @staticmethod
    def logout():
        logout_user()
        return True