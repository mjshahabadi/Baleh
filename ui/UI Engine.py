class UIEngine:

    @staticmethod
    def build(menu_name, keyboard_type, user):

        raw = UIRepository.get_menu(menu_name, keyboard_type)

        buttons = []

        for r in raw:

            btn = {
                "text": r[0],
                "icon": r[1],
                "action": r[2],
                "row": int(r[3]),
                "col": int(r[4]),
                "type": r[5],
                "align": r[6],
                "role_required": r[7],
                "condition_expr": r[8],
                "version": r[9]
            }

            if RuleEngine.check(btn, user):
                buttons.append(btn)

        return buttons