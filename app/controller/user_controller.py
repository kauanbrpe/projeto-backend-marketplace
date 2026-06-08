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

user_update_schema = user_ns.model('UserUpdateInput', {
    'name': fields.String(required=False, description='Novo nome'),
    'email': fields.String(required=False, description='Novo e-mail'),
    'password': fields.String(required=False, description='Nova senha'),
    'endereco': fields.String(required=False, description='Novo endereço'),
    'is_admin': fields.Boolean(required=False, description='Status de administrador')
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

@user_ns.route('/<int:user_id>')
@user_ns.doc(params={'user_id': 'O identificador único do usuário'})
class UserDetail(Resource):

    @user_ns.expect(user_update_schema)
    @user_ns.doc(responses={200: 'Ok', 400: 'Invalid', 401: 'Unauthorized', 403: 'Forbidden', 404: 'Not Found'})
    @login_required
    def put(self, user_id):
        if current_user.id != user_id and not current_user.is_admin:
            return {"error": "Acesso negado: Você não pode editar dados de outro usuário."}, 403

        data = request.json
        if not data:
            return {"error": "Nenhum dado enviado para atualização."}, 400

        try:
            updated_user = UserService.update_user(user_id, data)
            return updated_user.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 404
        except Exception as e:
            return {"error": "Erro interno ao atualizar o usuário."}, 500

    @user_ns.doc(responses={200: 'Ok', 401: 'Unauthorized', 403: 'Forbidden', 404: 'Not Found'})
    @login_required
    def delete(self, user_id):
        if current_user.id != user_id and not current_user.is_admin:
            return {"error": "Acesso negado: Você não pode excluir a conta de outro usuário."}, 403

        try:
            UserService.delete_user(user_id)
            return {"message": "Usuário excluído com sucesso."}, 200
        except ValueError as e:
            return {"error": str(e)}, 404
        except Exception as e:
            return {"error": "Erro interno ao excluir o usuário."}, 500
