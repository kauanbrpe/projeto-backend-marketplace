from app.models.product_model import ProductModel
from app.repository import ProductRepository

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

        return ProductRepository.save(novo_produto)

    @staticmethod
    def listar_produtos():
        products = ProductRepository.get_all()
        return [product.to_dict() for product in products]

    @staticmethod
    def listar_produto_por_id(product_id):
        product = ProductRepository.find_by_id(product_id)
        if not product:
            raise ValueError("Erro: Produto não encontrado!")
        return product.to_dict()

    @staticmethod
    def listar_produto_por_user_id(user_id):
        product = ProductRepository.find_by_user_id(user_id)
        if not product:
            raise ValueError("Erro: Produto não encontrado!")
        return product.to_dict()