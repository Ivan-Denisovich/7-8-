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
import streamlit as st
from application import app
from domain import User
from infrastructure import get_products_with_return_option


def logout() -> Never:
    exit()


def render_main_page(app_state):
    st.title("Главное меню")
    st.write("Выберите действие:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Войти в систему"):
            app_state["page"] = "auth"
            st.rerun()
    
    with col2:
        if st.button("Посмотреть информацию о приложении"):
            app_state["page"] = "info"
            st.rerun()
    
    with col3:
        if st.button("Выйти и завершить программу"):
            exit()

def render_auth_page(app_state):
    st.title("Авторизация")
    
    if st.button("Назад"):
        app_state["page"] = "main"
        st.rerun()

    with st.form("auth_form"):
        username = st.text_input("Логин")
        password = st.text_input("Пароль", type="password")
        
        col1, col2 = st.columns(2)
        
        with col1:
            submit = st.form_submit_button("Войти в систему")
        with col2:
            exit_btn = st.form_submit_button("Выйти из системы")
        if submit:
   
            match (username, password):
                case login, password  if not all([login, password]):
                    st.error("Заполните все поля")
        
                case _:          
                    result = app.auth.authenticate(username, password)
            
                    result = app.auth.authenticate(username, password)

                    if result[0]:  
                        user = result[1]
                        app_state["user"] = user  
                        app_state["page"] = "personal"
                        st.success(result[2])
                        st.rerun()
                    else:
                            st.error(result[2])  
        elif exit_btn:
            app_state["page"] = "main"
            st.rerun()

def render_personal_page(app_state):
    st.title("Личный кабинет")
    
    user = app_state.get("user")
    
    if not user:
        st.error("Пользователь не авторизован")
        app_state["page"] = "auth"
        st.rerun()
        return

    st.subheader("Информация о пользователе")
    st.write(f"**Логин:** {user.username}")  
    st.write(f"**Email:** {user.email}")
    st.write(f"**Баланс:** {user.balance}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🛒 Перейти в магазин"):
            app_state["page"] = "shop"
            st.rerun()
    
    with col2:
        if st.button(" Выйти из учетной записи"):
            app_state["user"] = None
            app_state["page"] = "auth"
            st.success("Вы вышли из учетной записи")
            st.rerun()
    
    
   
def render_shop_page(app_state):
    st.title("Магазин")
    
    user = app_state.get("user")
    
    if not user:
        st.error("Необходимо авторизоваться")
        app_state["page"] = "auth"
        st.rerun()
        return
    
    
    st.info(f"Ваш баланс: **{user.balance} руб.**")
    
    
    products = get_products_with_return_option()
    
    
    st.subheader("Выберите товар:")
    
    for i, product in enumerate(products):
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            st.write(f"**{i+1}) {product.name}**")
        
        with col2:
            if product.price > 0:
                st.write(f"**{product.price} руб.**")
        
        with col3:
            if st.button("Купить", key=f"buy_{i}"):
                if product.name == "Вернуться в личный кабинет":
                    app_state["page"] = "personal"
                    st.rerun()
                    return
                
               
                user_obj = User(
                    user_id=user["id"],
                    username=user["username"],
                    password="",
                    email=user["email"],
                    balance=user["balance"]
                )
                
              
                success, message = app.shop.make_purchase(user_obj, product)
                
                if success:
                    st.success(message)
                    
                    app_state["user"]["balance"] = user_obj.balance
                    st.rerun()
                else:
                    st.error(message)




def render_info_page(app_state):
    st.title("Информация о приложении")
    
    st.write("""
    ## Интернет-магазин "Чижик"!\n
    **Супермодное приложение для пяти пользователей**\n
    **DDD архитектура**\n
    **Оригинальный дизайн**\n
    **Удобный интерфейс** \n
    **Уникальный фирменный стиль**\n
       
    """)
    
    
    if st.button("Назад"):
        app_state["page"] = "main"
        st.rerun()