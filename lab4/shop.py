from products import Product
from orders import OrderManager

class Shop:
    def __init__(self):
        self.products = []
        self.order_manager = OrderManager()

    def add_product(self, name, price, quantity):
        new_product = Product(name, price, quantity)
        self.products.append(new_product)

    def get_product(self, product_name):
        """Получить товар по имени."""
        for product in self.products:
            if product.name == product_name:
                return product
        raise ValueError(f"Товар с именем {product_name} не найден")  # Исключение для ошибки

    def check_product_availability(self, product, quantity):
        """Проверка, есть ли достаточное количество товара."""
        if product.quantity < quantity:
            raise ValueError(f"Недостаточно товара на складе. Доступно {product.quantity} единиц.")

    def place_order(self, product_name, quantity):
        try:
            product = self.get_product(product_name)
            self.check_product_availability(product, quantity)

            # Создание заказа
            product.quantity -= quantity
            order = self.order_manager.create_order(product_name, quantity, product.price)
            return f"Заказ оформлен: {order.quantity} x {order.product_name} на сумму {order.total_price}"

        except ValueError as e:
            return str(e)  # Возвращаем ошибку как строку, если возникло исключение

    def show_orders(self):
        """Отобразить все заказы."""
        self.order_manager.list_orders()
