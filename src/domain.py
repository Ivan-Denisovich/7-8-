# ===--- domain.py -------------------------------------------------------=== #
#
# Это модуль для реализации Domain Layer.
#
# Смысл его в том, чтобы описать модели, с которыми будет работать приложение.
# Например, пользователь, продукт, квартира, машина и т. д.  Эти модели
# содержат в себе свойства (баланс, цена, цвет и т. д.) и бизнес-правила,
# на которых держится приложение.  Например, в модели пользователя можно
# проверить, достаточно ли у него денег для покупки товара,а в модели
# товара - есть ли он на складе.
#
# ===---------------------------------------------------------------------=== #

class User:
    def __init__(self, user_id, username, password, email, balance):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.email = email
        self.balance = balance

class Product:
    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price