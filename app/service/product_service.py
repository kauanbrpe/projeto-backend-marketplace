from app.models.product_model import ProductModel
from app import db

class ProductService:
    @staticmethod
    def criar_produto(dados):
        
        if dados.get('price', 0) <= 0:
            raise ValueError("Erro: O preço deve ser maior que R$ 0,00!")

        
        if dados.get('stock', 0) < 0:
            raise ValueError("Erro: O estoque não pode ser negativo!")

        
        novo_produto = ProductModel(
            name=dados['name'],
            price=dados['price'],
            stock=dados['stock'],
            category_id=dados['category_id'],
            seller_id=dados['seller_id']
        )

        db.session.add(novo_produto)
        db.session.commit()
        return novo_produto