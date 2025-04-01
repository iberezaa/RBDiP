import unittest
from shop import Shop
from orders import OrderManager
from products import Product

class TestShop(unittest.TestCase):

    def setUp(self):
        """Создаёт тестовый магазин перед каждым тестом"""
        self.shop = Shop()
        self.shop.add_product("Телефон", 50000, 10)
        self.shop.add_product("Ноутбук", 80000, 5)

    def test_add_product(self):
        """Тест добавления товаров"""
        self.shop.add_product("Планшет", 30000, 7)
        product = self.shop.get_product("Планшет")
        self.assertIsNotNone(product)
        self.assertEqual(product.price, 30000)
        self.assertEqual(product.quantity, 7)

    def test_place_order_success(self):
        """Тест успешного оформления заказа"""
        result = self.shop.place_order("Телефон", 2)
        self.assertEqual(result, "Заказ оформлен: 2 x Телефон на сумму 100000")

        product = self.shop.get_product("Телефон")
        self.assertEqual(product.quantity, 8)

    def test_place_order_insufficient_stock(self):
        """Тест оформления заказа при недостаточном количестве товара"""
        result = self.shop.place_order("Ноутбук", 10)
        self.assertEqual(result, "Недостаточно товара на складе")

    def test_place_order_product_not_found(self):
        """Тест оформления заказа на несуществующий товар"""
        result = self.shop.place_order("Камера", 1)
        self.assertEqual(result, "Товар не найден")

    def test_product_negative_values(self):
        """Тест попытки создания товара с отрицательной ценой или количеством"""
        with self.assertRaises(ValueError):
            Product("Часы", -1000, 5)
        with self.assertRaises(ValueError):
            Product("Часы", 1000, -5)

    def test_order_manager_create_order(self):
        """Тест создания заказа через OrderManager"""
        order_manager = OrderManager()
        order = order_manager.create_order("Мышка", 2, 1500)
        self.assertEqual(order.product_name, "Мышка")
        self.assertEqual(order.quantity, 2)
        self.assertEqual(order.total_price, 3000)

if __name__ == '__main__':
    unittest.main()
