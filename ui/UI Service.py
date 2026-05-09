class UIService:

    @staticmethod
    def build(menu_name, keyboard_type, user):

        buttons = UIEngine.build(menu_name, keyboard_type, user)

        rows = LayoutEngine.group(buttons)

        if keyboard_type == "reply":
            return KeyboardRenderer.reply(rows)

        return KeyboardRenderer.inline(rows)