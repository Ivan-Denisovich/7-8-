# ===--- infrastructure.py -----------------------------------------------=== #
#
# Это модуль для реализации Infrastructure Layer.
#
# Его задача состоит в том, чтобы выполнить определенные действия, связанные с
# внешним миром.  Например, отправить данные в базу, закодировать пароль по
# определенному принципу, получить какую-то картинку из интернета и т. д.
# Этот слой - исполнитель, он делает то, что ему говорит Application Layer и
# отдает ему результат.
#
# ===---------------------------------------------------------------------=== 
import csv
from domain import User, Product


USERS_CSV = "data/user.csv"  
PRODUCTS_CSV = "data/product.csv" 


def get_user_by_credentials(username, password):
    with open(USERS_CSV, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        
        for row in reader:
            if row[1] == username and row[2] == password:
                return User(
                    user_id=row[0],
                    username=row[1],
                    password=row[2],
                    email=row[3],
                    balance=float(row[4])
                )
    return None

def get_user_by_username(username):
    with open(USERS_CSV, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        
        for row in reader:
            if row[1] == username:
                return User(
                    user_id=row[0],
                    username=row[1],
                    password=row[2],
                    email=row[3],
                    balance=float(row[4])
                )
    return None

def refresh_user_balance(user_id, new_balance):
  
    rows = []
    updated = False

    with open(USERS_CSV, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)

        for row in reader:
            if row[0] == user_id:
                row[4] = str(new_balance)
                updated = True
            rows.append(row)

def get_all_products():
    products = []
    with open(PRODUCTS_CSV, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader, 1):
            products.append(Product(
                product_id=str(i),
                name=row['name'],
                price=float(row['price'])
            ))
    return products

def get_products_with_return_option():
    from infrastructure import get_all_products
    products = get_all_products()
    products.append(Product("return", "Вернуться в личный кабинет", 0.0))
    return products



    


