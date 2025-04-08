class Product:
    def __init__(self, name, price, quantity):
        if price < 0 or quantity < 0:
            raise ValueError("Цена и количество должны быть неотрицательными")
        self.name = name
        self.price = price
        self.quantity = quantity
