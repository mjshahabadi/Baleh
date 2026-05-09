from db.database import db_conn


class UIService:

    @staticmethod
    def get_menu(menu_name: str, keyboard_type: str = "inline"):
        with db_conn() as conn:
            cur = conn.cursor()

            cur.execute("""
                SELECT button_text, icon, callback_data,
                       row_index, col_index, row_align, keyboard_type
                FROM baleh.bot_buttons
                WHERE menu_name=? AND keyboard_type=?
                ORDER BY row_index, col_index
            """, (menu_name, keyboard_type))

            rows = cur.fetchall()

        buttons = []
        final_keyboard_type = "inline"

        for r in rows:
            buttons.append({
                "title": str(r[0]),
                "icon": str(r[1] or ""),
                "action": str(r[2]),
                "row": int(r[3]),
                "col": int(r[4]),
                "align": str(r[5] or "right")
            })

            final_keyboard_type = str(r[6] or keyboard_type)

        return buttons, final_keyboard_type