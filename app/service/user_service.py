from app.models import UserModel
from app.repository import UserRepository
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user

class UserService:
    @staticmethod
    def user_registration(data):
        if not data.get("name") or not data.get("email") or not data.get("password") or not data.get("endereco"):
            raise ValueError("Error: Name, email, password and endereco required.")

        existing_user = UserRepository.find_by_email(data['email'])
        if existing_user:
            raise ValueError("Error: Email already exists.")

        new_user = UserModel(
            name=data['name'],
            email=data['email'],
            endereco=data['endereco'],
            password_hash=generate_password_hash(data['password']),
            is_admin=data.get('is_admin', False)
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

    @staticmethod
    def update_user(user_id, data):
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise ValueError("Error: User not found.")

        if data.get('name'):
            user.name = data['name']
        if data.get('email'):
            existing = UserRepository.find_by_email(data['email'])
            if existing and existing.id != user_id:
                raise ValueError("Error: Email already in use.")
            user.email = data['email']
        if data.get('endereco'):
            user.endereco = data['endereco']
        if data.get('password'):
            user.password_hash = generate_password_hash(data['password'])
        if 'is_admin' in data:
            user.is_admin = data['is_admin']

        return UserRepository.update_user(user)

    @staticmethod
    def delete_user(user_id):
        user = UserRepository.find_by_id(user_id)
        if not user:
            raise ValueError("Error: User not found.")
        UserRepository.delete_user(user_id)
        return True
