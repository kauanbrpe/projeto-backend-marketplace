from flask import request
from flask_restx import Namespace, Resource, fields
from flask_login import login_required, current_user
from app.service import UserService

user_ns = Namespace('users', description='Operações relacionadas à autenticação e gerenciamento de usuários')

user_register_schema = user_ns.model('UserRegisterInput', {
    'name': fields.String(required=True, description='Nome completo do usuário', example='João Silva'),
    'email': fields.String(required=True, description='Endereço de e-mail único', example='joao@email.com'),
    'password': fields.String(required=True, description='Senha de acesso', example='senha123'),
    'endereco': fields.String(required=True, description='Endereço residencial', example='Rua das Flores, 123'),
    'is_admin': fields.Boolean(required=False, description='Define se o usuário é administrador', default=False)
})

user_login_schema = user_ns.model('UserLoginInput', {
    'email': fields.String(required=True, description='E-mail cadastrado', example='joao@email.com'),
    'password': fields.String(required=True, description='Senha cadastrada', example='senha123')
})

user_output_schema = user_ns.model('UserOutput', {
    'id': fields.Integer(description='ID único do usuário'),
    'name': fields.String(description='Nome completo'),
    'email': fields.String(description='E-mail'),
    'endereco': fields.String(description='Endereço'),
    'is_admin': fields.Boolean(description='Status de administrador')
})

@user_ns.route('/register')
class UserRegister(Resource):

    @user_ns.expect(user_register_schema)
    @user_ns.doc(responses={201: 'Created', 400: 'Invalid'})
    def post(self):
        data = request.json

        try:
            new_user = UserService.user_registration(data)
            return new_user.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": "Erro interno ao registrar usuário"}, 500

@user_ns.route('/login')
class UserLogin(Resource):

    @user_ns.expect(user_login_schema)
    @user_ns.doc(responses={200: 'Ok', 400: 'Invalid'})
    def post(self):
        data = request.json

        if not data or 'email' not in data or 'password' not in data:
            return {"error": "E-mail e senha são obrigatórios"}, 400

        try:
            usuario = UserService.log_in(data['email'], data['password'])
            return {
                "message": "Logged in successfully.",
                "user": usuario.to_dict()
            }, 200
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": "Erro interno ao realizar login"}, 500

@user_ns.route('/logout')
class UserLogout(Resource):

    @user_ns.doc(responses={200: 'Ok', 401: 'Unauthorized'})
    @login_required
    def post(self):

        try:
            UserService.logout()
            return {"message": "Logged out successfully."}, 200
        except Exception as e:
            return {"error": "Erro interno ao realizar logout"}, 500

@user_ns.route('/me')
class UserProfile(Resource):

    @user_ns.doc(responses={200: 'Ok', 401: 'Unauthorized'})
    @user_ns.marshal_with(user_output_schema)
    @login_required
    def get(self):
        return current_user, 200