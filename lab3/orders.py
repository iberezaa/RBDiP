class Order:
    def __init__(self, product_name, quantity, total_price):
        self.product_name = product_name
        self.quantity = quantity
        self.total_price = total_price

class OrderManager:
    def __init__(self):
        self.orders = []

    def create_order(self, product_name, quantity, price):
        """Создает новый заказ и добавляет его в список"""
        order = Order(product_name, quantity, price * quantity)
        self.orders.append(order)
        return order

    def list_orders(self):
        """Выводит список всех заказов"""
        if not self.orders:
            print("Заказов пока нет")
        for order in self.orders:
            print(f"Заказ: {order.product_name}, Количество: {order.quantity}, Сумма: {order.total_price}")
