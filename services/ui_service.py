from db.database import db_conn


class UIService:
    """Database-backed menu and button lookup service."""

    DEFAULT_KEYBOARD_TYPE = "inline"

    @staticmethod
    def get_menu(menu_name):
        """Return active menu metadata and active buttons for ``menu_name``.

        The return shape is intentionally stable for the keyboard builder and
        message handler::

            {
                "menu": {"menu_name": ..., "keyboard_type": ..., "title": ...},
                "buttons": [{"text": ..., "icon": ..., "callback_data": ..., ...}]
            }
        """

        with db_conn() as conn:
            cur = conn.cursor()

            cur.execute(
                """
                SELECT
                    menu_name,
                    keyboard_type,
                    title
                FROM baleh.menus
                WHERE menu_name = ?
                  AND ISNULL(is_active, 1) = 1
                """,
                (menu_name,),
            )

            menu = cur.fetchone()

            if not menu:
                return None

            menu_data = {
                "menu_name": str(menu[0]),
                "keyboard_type": str(menu[1] or UIService.DEFAULT_KEYBOARD_TYPE),
                "title": str(menu[2] or "📋 منو"),
            }

            cur.execute(
                """
                SELECT
                    button_text,
                    icon,
                    callback_data,
                    row_index,
                    col_index,
                    row_align
                FROM baleh.bot_buttons
                WHERE menu_name = ?
                  AND ISNULL(is_active, 1) = 1
                ORDER BY row_index, col_index
                """,
                (menu_name,),
            )

            rows = cur.fetchall()

        buttons = [UIService._button_from_row(row) for row in rows]

        return {
            "menu": menu_data,
            "buttons": buttons,
        }

    @staticmethod
    def get_menu_by_text(button_text):
        """Resolve a reply-keyboard button caption to a target menu name.

        Reply keyboard updates only include the displayed text, so this method
        searches active buttons by plain text and icon-prefixed display text. It
        returns the menu target when the button callback is either ``MENU:name``
        or a DB route whose type is ``menu``.
        """

        normalized_text = UIService._normalize_text(button_text)
        if not normalized_text:
            return None

        with db_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT TOP 1
                    b.callback_data,
                    r.route_type,
                    r.route_value
                FROM baleh.bot_buttons b
                LEFT JOIN baleh.routes r
                       ON r.callback_data = b.callback_data
                      AND ISNULL(r.is_active, 1) = 1
                INNER JOIN baleh.menus m
                        ON m.menu_name = b.menu_name
                       AND ISNULL(m.is_active, 1) = 1
                WHERE ISNULL(b.is_active, 1) = 1
                  AND (
                        LTRIM(RTRIM(b.button_text)) = ?
                     OR LTRIM(RTRIM(CONCAT(ISNULL(b.icon, ''),
                           CASE WHEN ISNULL(b.icon, '') = '' THEN '' ELSE ' ' END,
                           b.button_text))) = ?
                  )
                ORDER BY b.row_index, b.col_index
                """,
                (normalized_text, normalized_text),
            )
            row = cur.fetchone()

        if not row:
            return None

        callback_data = str(row[0] or "")
        route_type = str(row[1] or "").lower()
        route_value = row[2]

        if callback_data.startswith("MENU:"):
            return callback_data.split(":", 1)[1]

        if route_type == "menu" and route_value:
            return str(route_value)

        return None

    @staticmethod
    def _button_from_row(row):
        return {
            "text": str(row[0]),
            "icon": str(row[1] or ""),
            "callback_data": str(row[2] or ""),
            "row": int(row[3] or 0),
            "col": int(row[4] or 0),
            "align": str(row[5] or "right"),
        }

    @staticmethod
    def _normalize_text(value):
        return str(value or "").strip()
