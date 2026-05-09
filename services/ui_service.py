from db.database import db_conn


class UIService:

    # =====================================================
    # GET MENU
    # =====================================================
    @staticmethod
    def get_menu(menu_name):

        with db_conn() as conn:

            cur = conn.cursor()

            # ==========================================
            # MENU META
            # ==========================================
            cur.execute("""
                SELECT
                    menu_name,
                    keyboard_type,
                    title
                FROM baleh.menus
                WHERE menu_name = ?
                  AND is_active = 1
            """, (menu_name,))

            menu = cur.fetchone()

            if not menu:
                return None

            menu_data = {
                "menu_name": menu[0],
                "keyboard_type": menu[1],
                "title": menu[2]
            }

            # ==========================================
            # BUTTONS
            # ==========================================
            cur.execute("""
                SELECT
                    button_text,
                    icon,
                    callback_data,
                    row_index,
                    col_index,
                    row_align
                FROM baleh.bot_buttons
                WHERE menu_name = ?
                ORDER BY row_index, col_index
            """, (menu_name,))

            rows = cur.fetchall()

        buttons = []

        for r in rows:

            buttons.append({
                "text": str(r[0]),
                "icon": str(r[1] or ""),
                "callback_data": str(r[2]),
                "row": int(r[3]),
                "col": int(r[4]),
                "align": str(r[5] or "right")
            })

        return {
            "menu": menu_data,
            "buttons": buttons
        }