# ===--- application.py --------------------------------------------------=== #
#
# Это модуль для реализации Application Layer.
#
# Суть его состоит в том, чтобы описать логические действия, которые возможны
# в приложении.  В этой работе он может импортировать модули инфраструктуры,
# но смысл этого модуля - именно описать, что можно делать в приложении.
# Например, зарегистрироваться, сделать заказ, обновить данные профиля.  Для
# этого модуль может вызвать инфраструктурные методы, в которых содержится
# непосредственно реализация функционала.  Таким образом, будет получаться
# логическая цепочка, не привязанная к реализации.
#
# ===---------------------------------------------------------------------=== #
from infrastructure import (
    get_user_by_credentials,
    get_user_by_username,
    refresh_user_balance,
    get_products_with_return_option,
)

class Authentication:
    def authenticate(self, username, password):
        if not username or not password:
            return False, None, "Заполните поля"
        
        user = get_user_by_credentials(username, password)
        
        if user:
            return True, user, f"Добро пожаловать, {user.username}!"
        
        return False, None, "Неверный логин или пароль"

class Shop:
    
    
    def make_purchase(self, user, product):
        if product.name == "Вернуться в личный кабинет":
            return False, "return_to_personal"
        
        if user.balance < product.price:
            return False, f"Недостаточно денег для покупки '{product.name}'"
        
        user.balance -= product.price
        refresh_user_balance(user.user_id, user.balance)
        return True, f"Товар '{product.name}' успешно приобретен!"

class UserProfile:
    def get_user_info(self, username):
        user = get_user_by_username(username)
        
        if not user:
            return False, None, "Пользователь не найден"
        
        return True, {
            'username': user.username,
            'email': user.email,
            'balance': user.balance
        }, ""

class Application:
    def __init__(self):
        self.auth = Authentication()
        self.shop = Shop()
        self.profile = UserProfile()

app = Application()