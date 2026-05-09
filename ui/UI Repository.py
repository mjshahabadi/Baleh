class UIRepository:

    @staticmethod
    def get_menu(menu_name, keyboard_type):

        with db_conn() as conn:
            cur = conn.cursor()

            cur.execute("""
                SELECT button_text, icon, callback_data,
                       row_index, col_index,
                       keyboard_type, align,
                       role_required, condition_expr, version
                FROM baleh.bot_buttons
                WHERE menu_name=? AND keyboard_type=? AND is_active=1
                ORDER BY priority DESC, row_index, col_index
            """, (menu_name, keyboard_type))

            return cur.fetchall()