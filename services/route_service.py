from db.database import db_conn


class RouteService:

    @staticmethod
    def resolve(callback_data: str):

        """
        همه routing از DB میاد (Enterprise Mode)
        """

        with db_conn() as conn:
            cur = conn.cursor()

            cur.execute("""
                SELECT route_type, route_value
                FROM baleh.routes
                WHERE callback_data = ?
            """, (callback_data,))

            row = cur.fetchone()

        if not row:
            return "action", callback_data

        return row[0], row[1]