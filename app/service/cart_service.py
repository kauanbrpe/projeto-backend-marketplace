from app.repository import CartRepository
from app.models import CartModel
from app.repository import ProductRepository

class CartService:
    @staticmethod
    def get_or_create_cart(current_user):
        if not current_user.is_authenticated:
            raise PermissionError("Access denied: You need to be logged in.")

        cart = CartRepository.find_by_user_id(current_user.id)
        if not cart:
            new_cart = CartModel(user_id=current_user.id)
            cart = CartRepository.save(new_cart)

        return cart.to_dict()

    @staticmethod
    def add_product(product_id, quantity, current_user):
        if not current_user.is_authenticated:
            raise PermissionError("Access denied: You need to be logged in.")

        if quantity <= 0:
            raise ValueError("Error: Quantity must be greater than 0.")

        product = ProductRepository.find_by_id(product_id)
        if not product:
            raise ValueError("Error: Product not found.")
        if product.stock < quantity:
            raise ValueError(f"Error: Product stock is lower than quantity. Quantity: {product.stock}")

        cart = CartRepository.find_by_user_id(current_user.id)
        if not cart:
            new_cart = CartModel(user_id=current_user.id)
            cart = CartRepository.save(new_cart)

        current_quantity = CartRepository.get_item_quantity(cart.id, product_id)
        if current_quantity is not None:
            new_quantity = current_quantity + quantity
            if product.stock < new_quantity:
                raise ValueError(f"Error: Product stock is lower than quantity. Quantity: {product.stock}")
            CartRepository.update_item_quantity(cart.id, product_id, quantity)
        else:
            CartRepository.add_item(cart.id, product_id, quantity)

        return CartRepository.find_by_user_id(current_user.id).to_dict()

    @staticmethod
    def remove_product(product_id, current_user):
        if not current_user.is_authenticated:
            raise PermissionError("Access denied: You need to be logged in.")

        cart = CartRepository.find_by_user_id(current_user.id)
        if not cart:
            raise ValueError("Error: Cart not found.")

        CartRepository.remove_item(cart.id, product_id)
        return CartRepository.find_by_user_id(current_user.id).to_dict()

    @staticmethod
    def add_coupon_cart (code_coupon, current_user):
        if not current_user.is_authenticated:
            raise PermissionError("Access denied: You need to be logged in.")

        #TODO Importar o CouponService aqui
        from app.service import CouponService

        cart_obj = CartRepository.find_by_user_id(current_user.id)

        if not cart_obj or not cart_obj.products:
            raise ValueError("Error: Cart not found.")

        valor_total_bruto = sum(float(produto.price) for produto in cart_obj.products)

        valor_desconto = CouponService.validar_e_calcular_desconto(code_coupon, valor_total_bruto)

        if valor_desconto is None or valor_desconto <= 0:
            raise ValueError("Error: Valor desconto invalido.")

        valor_final_com_desconto = valor_total_bruto - valor_desconto

        return {
            "mensagem": f"Cupom {code_coupon.upper()} aplicado com sucesso!",
            "subtotal": round(valor_total_bruto, 2),
            "desconto_aplicado": round(valor_desconto, 2),
            "total_a_pagar": round(max(0.0, valor_final_com_desconto), 2)
        }