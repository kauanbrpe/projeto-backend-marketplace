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
        return ProductRepository.get_all()

    @staticmethod
    def listar_produto_por_id(product_id):
        product = ProductRepository.find_by_id(product_id)
        if not product:
            raise ValueError("Erro: Produto não encontrado!")
        return product

    @staticmethod
    def listar_produto_por_user_id(user_id):
        products = ProductRepository.find_by_user_id(user_id)
        if not products:
            raise ValueError("Erro: Nenhum produto encontrado para este usuário!")
        return products

    @staticmethod
    def atualizar_produto(product_id, dados, current_user):
        product = ProductRepository.find_by_id(product_id)
        if not product:
            raise ValueError("Erro: Produto não encontrado!")

        if product.seller_id != current_user.id and not current_user.is_admin:
            raise PermissionError("Acesso negado: Você não pode editar um produto de outro vendedor.")

        if 'name' in dados:
            product.name = dados['name']
        if 'price' in dados:
            if dados['price'] <= 0:
                raise ValueError("Erro: O preço deve ser maior que R$ 0,00!")
            product.price = dados['price']
        if 'stock' in dados:
            if dados['stock'] < 0:
                raise ValueError("Erro: O estoque não pode ser negativo!")
            product.stock = dados['stock']
        if 'category_id' in dados:
            product.category_id = dados['category_id']

        return ProductRepository.update(product)

    @staticmethod
    def delete_product(product_id, current_user):
        product = ProductRepository.find_by_id(product_id)
        if not product:
            raise ValueError("Erro: Produto não encontrado!")

        if product.seller_id != current_user.id and not current_user.is_admin:
            raise PermissionError("Acesso negado: Você não pode excluir um produto de outro vendedor.")

        ProductRepository.delete(product)
        return True
