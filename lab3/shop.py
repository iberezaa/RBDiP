from products import Product
from orders import OrderManager

class Shop:
    def __init__(self):
        self.products = []
        self.order_manager = OrderManager()

    def add_product(self, name, price, quantity):
        if price < 0 or quantity < 0:
            raise ValueError("Цена и количество не могут быть отрицательными")
        new_product = Product(name, price, quantity)
        self.products.append(new_product)

    def get_product(self, product_name):
        for product in self.products:
            if product.name == product_name:
                return product
        return None

    def place_order(self, product_name, quantity):
        product = self.get_product(product_name)
        if product is None:
            return "Товар не найден"
        if product.quantity < quantity:
            return "Недостаточно товара на складе"

        product.quantity -= quantity
        order = self.order_manager.create_order(product_name, quantity, product.price)
        return f"Заказ оформлен: {order.quantity} x {order.product_name} на сумму {order.total_price}"

    def show_orders(self):
        self.order_manager.list_orders()
