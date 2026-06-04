from app.models.category_model import CategoryModel
from app.repository import CategoryRepository


class CategoryService:
    @staticmethod
    def criar_categoria(dados):
        
        if not dados.get('name'):
            raise ValueError("Erro: O nome da categoria é obrigatório!")

        nova_categoria = CategoryModel(
            name=dados['name']
        )

        return CategoryRepository.save(nova_categoria)