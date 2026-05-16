from db.database import db_conn


class PlanService:

    @staticmethod
    def get_active_plans():
        with db_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT Id, title, Price, duration_days
                FROM baleh.Plans
                WHERE ISNULL(IsActive, 1) = 1
                ORDER BY Id
            """)

            rows = cur.fetchall()

            return [
                {
                    "id": r[0],
                    "name": r[1],
                    "price": r[2],
                    "duration": r[3]
                }
                for r in rows
            ]
