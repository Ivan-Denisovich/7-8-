# ===--- ui.py -----------------------------------------------------------=== #
#
# Это модуль для реализации Presentation Layer.
#
# Его задача - просто отрисовать то, что должен видеть пользователь.  Он может
# вызывать действия, описанные в Application Layer и результат выполнения этих
# действий отображать пользователю.  Никакой бизнес-логики в слое представления
# быть не может.  Единственное, что можно делать - проверять валидность данных,
# которые вводит пользователь.  Например, все ли поля заполнены или проверка,
# не ввел ли пользователь мусор.  Если проверка затрагивает бизнес-правила, то
# выполнять ее следует в других слоях.
#
# ===---------------------------------------------------------------------=== #
from typing import Never
from application import app
from domain import User
from infrastructure import get_products_with_return_option


def logout() -> Never:
    exit()



def render_main_page(app_state):
    print("ГЛАВНОЕ МЕНЮ")
    print("="*40)
    print("1. Войти в систему")
    print("2. Информация о приложении")
    print("3. Выйти")
    choose = input("Выберите пункт (1-3): ").strip()

    match choose:
        case "1":
            app_state["page"] = "auth"
        case "2":
            app_state["page"] = "info"
        case "3":
            exit()

def render_auth_page(app_state):
    print("\n" + "="*40)
    print(" АВТОРИЗАЦИЯ")
    print("="*40)
    
    while True:
        print("\n1. Ввести логин/пароль")
        print("2. Назад в главное меню")
        print("3. Выйти из системы")
        
        choose = input("Выберите действие (1-3): ").strip()
        match choose:
            case "1":
                username = input("Логин: ").strip()
                password = input("Пароль: ").strip()
            
            
                result = app.auth.authenticate(username, password)
            
                if result[0]: 
                    user = result[1]
                    app_state["user"] = user
                    app_state["page"] = "personal"
                    print(f"{result[2]}")
                    break
                else:
                    print(f"{result[2]}")
                
            case "2":
                app_state["page"] = "main"
                break
            
            case "3":
                print(" До свидания!")
                exit()
            case _:
                print("ERROR!")

def render_personal_page(app_state):
    user = app_state.get("user")
    
    if not user:
        print(" Пользователь не авторизован")
        app_state["page"] = "auth"
        return

    print(" ЛИЧНЫЙ КАБИНЕТ")
    print("="*40)
    print(f"Логин: {user.username}")
    print(f"Email: {user.email}")
    print(f"Баланс: {user.balance} руб.")
    
    print("\n1.  Перейти в магазин")
    print("2.  Выйти из учетной записи")
    
    choose = input("Выберите действие (1-2): ").strip()
    match choose:
        case "1":
            app_state["page"] = "shop"
        case "2":
            app_state["user"] = None
            app_state["page"] = "auth"
            print("Вы вышли из учётной записи")
        case _:
            print("ERROR!!")


    
   
def render_shop_page(app_state):
    user = app_state.get("user")
    
    if not user:
        print("Войдите сначала")
        app_state["page"] = "auth"
        return
    
    print(f"Баланс: {user.balance} руб.")
    print("\nТовары:")
    
    products = get_products_with_return_option()
    
    for i, p in enumerate(products):
        print(f"{i+1}. {p.name} - {p.price} руб.")
    
    try:
        n = int(input("Номер товара: "))
        if n < 1 or n > len(products):
            return
            
        product = products[n-1]
        
        if product.name == "Вернуться в личный кабинет":
            app_state["page"] = "personal"
            return
        
    
        
        ok, prod = app.shop.make_purchase(user, product)
        
        if ok:
            print(f"Куплено: {prod}")
            app_state["user"]["balance"] = user.balance
        else:
            print(f"Не куплено: {prod}")
            
    except:
        print("Ошибка ввода")


def render_info_page(app_state):
    print("\nИнформация о приложении:")
    print("Интернет-магазин 'Чижик'!")
    print("- Супермодное приложение для пяти пользователей")
    print("- DDD архитектура")
    print("- Оригинальный дизайн")
    print("- Удобный интерфейс")
    print("- Уникальный фирменный стиль")
    
    input("\nНажмите Enter для возврата...")
    app_state["page"] = "main"