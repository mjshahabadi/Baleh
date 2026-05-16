from datetime import datetime, timedelta
from db.database import db_conn


class SubscriptionService:

    @staticmethod
    def get_active(user_id):
        with db_conn() as conn:
            cur = conn.cursor()

            cur.execute("""
                SELECT TOP 1 end_date
                FROM baleh.Subscriptions
                WHERE user_id = ?
                  AND ISNULL(is_active, 1) = 1
                ORDER BY end_date DESC
            """, (user_id,))

            row = cur.fetchone()

            if not row:
                return False

            return row[0] > datetime.utcnow()

    @staticmethod
    def create(user_id, plan_days, plan_id=None):
        start = datetime.utcnow()
        end = start + timedelta(days=int(plan_days))

        with db_conn() as conn:
            cur = conn.cursor()

            cur.execute("""
                UPDATE baleh.Subscriptions
                SET is_active = 0
                WHERE user_id = ?
            """, (user_id,))

            cur.execute("""
                INSERT INTO baleh.Subscriptions
                    (user_id, plan_id, start_date, end_date, is_active)
                VALUES (?, ?, ?, ?, 1)
            """, (user_id, plan_id, start, end))

            conn.commit()

        return end

    @staticmethod
    def create_subscription(user_id, plan_id):
        with db_conn() as conn:
            cur = conn.cursor()

            cur.execute("""
                SELECT duration_days
                FROM baleh.Plans
                WHERE Id = ?
                  AND ISNULL(IsActive, 1) = 1
            """, (plan_id,))

            plan = cur.fetchone()

        if not plan:
            return False, "پلن اشتراک پیدا نشد یا غیرفعال است."

        end = SubscriptionService.create(
            user_id=user_id,
            plan_days=plan[0],
            plan_id=plan_id,
        )

        return True, end
