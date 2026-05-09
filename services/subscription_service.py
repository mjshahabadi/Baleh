from datetime import datetime, timedelta
from db.database import db_conn

class SubscriptionService:

    @staticmethod
    def get_active(user_id):
        with db_conn() as conn:
            cur = conn.cursor()

            cur.execute("""
                SELECT TOP 1 end_date
                FROM baleh.subscriptions
                WHERE user_id=? AND is_active=1
                ORDER BY end_date DESC
            """, (user_id,))

            row = cur.fetchone()

            if not row:
                return False

            return row[0] > datetime.utcnow()

    @staticmethod
    def create(user_id, plan_days):
        start = datetime.utcnow()
        end = start + timedelta(days=plan_days)

        with db_conn() as conn:
            cur = conn.cursor()

            # deactivate old
            cur.execute("""
                UPDATE baleh.ubscriptions
                SET is_active=0
                WHERE user_id=?
            """, (user_id,))

            # create new
            cur.execute("""
                INSERT INTO baleh.subscriptions
                (user_id, start_date, end_date, is_active)
                VALUES (?, ?, ?, 1)
            """, (user_id, start, end))

            conn.commit()

        return end