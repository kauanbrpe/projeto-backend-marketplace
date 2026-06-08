from app.models.category_model import CategoryModel
from app.repository import CategoryRepository

class CategoryService:
    @staticmethod
    def listar_todas():
        return CategoryRepository.find_all()

    @staticmethod
    def listar_por_id(category_id):
        return CategoryRepository.find_by_id(category_id)

    @staticmethod
    def criar_categoria(dados):
        if not dados.get('name'):
            raise ValueError("Erro: O nome da categoria é obrigatório!")

        nova_categoria = CategoryModel(name=dados['name'])
        return CategoryRepository.save(nova_categoria)

    @staticmethod
    def atualizar_categoria(category_id, dados, current_user):
        if not current_user.is_admin:
            raise PermissionError("Acesso negado: Apenas administradores podem editar categorias.")

        categoria = CategoryRepository.find_by_id(category_id)
        if not categoria:
            raise ValueError("Erro: Categoria não encontrada!")

        if 'name' in dados and dados['name']:
            categoria.name = dados['name']

        return CategoryRepository.update(categoria)

    @staticmethod
    def deletar_categoria(category_id, current_user):
        if not current_user.is_admin:
            raise PermissionError("Acesso negado: Apenas administradores podem excluir categorias.")

        categoria = CategoryRepository.find_by_id(category_id)
        if not categoria:
            raise ValueError("Erro: Categoria não encontrada!")

        CategoryRepository.delete(categoria)
        return True
