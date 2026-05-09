from handlers.message_handler import send_menu

class MenuService:

    @staticmethod
    def open_menu(bot, chat_id, menu_name):
        send_menu(bot, chat_id, menu_name)