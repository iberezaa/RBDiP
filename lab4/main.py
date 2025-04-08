from shop import Shop

shop = Shop()

shop.add_product("Телефон", 50000, 10)
shop.add_product("Ноутбук", 80000, 5)

print(shop.place_order("Телефон", 2))
print(shop.place_order("Ноутбук", 3))

shop.show_orders()
