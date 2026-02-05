import ui
from global_state import GlobalState

app_state = GlobalState()
current_page = app_state.get("page", "main")
def main():
    
    while True:
        current_page = app_state.get("page", "main")
        match current_page:
            case "main":
                ui.render_main_page(app_state)
            case "auth":
                ui.render_auth_page(app_state)
            case "personal":
                ui.render_personal_page(app_state)
            case "shop":
                ui.render_shop_page(app_state)
            case "info":
                ui.render_info_page(app_state)
            case _:
                ui.render_main_page(app_state)

if __name__ == "__main__":
    main()