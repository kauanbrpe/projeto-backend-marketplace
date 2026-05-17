from app.models.category_model import CategoryModel
from app import db

class CategoryService:
    @staticmethod
    def criar_categoria(dados):
        
        if not dados.get('name'):
            raise ValueError("Erro: O nome da categoria é obrigatório!")

        nova_categoria = CategoryModel(
            name=dados['name']
        )

        db.session.add(nova_categoria)
        db.session.commit()
        return nova_categoria