from db.database import db_conn


class RouteService:

    @staticmethod
    def resolve(callback_data: str):

        """
        همه routing از DB میاد (Enterprise Mode)
        """

        route = RouteService.resolve_details(callback_data)

        if not route:
            return "action", callback_data

        return route["route_type"], route["route_value"]

    @staticmethod
    def resolve_details(callback_data: str):
        with db_conn() as conn:
            cur = conn.cursor()

            cur.execute("""
                SELECT route_type, route_value, route_config
                FROM baleh.routes
                WHERE callback_data = ?
                  AND ISNULL(is_active, 1) = 1
            """, (callback_data,))

            row = cur.fetchone()

        if not row:
            return None

        return {
            "callback_data": callback_data,
            "route_type": row[0],
            "route_value": row[1],
            "route_config": row[2],
        }
