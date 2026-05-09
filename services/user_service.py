from db.database import db_conn

class UserService:

    @staticmethod
    def get_or_create_user(message: dict):
        user_data = message.get("from", {})
        bale_user_id = str(user_data.get("id"))

        with db_conn() as conn:
            cur = conn.cursor()

            cur.execute("SELECT id FROM baleh.users WHERE bale_user_id = ?", (bale_user_id,))
            row = cur.fetchone()

            if row:
                return row[0]

            cur.execute("""
                INSERT INTO baleh.users (bale_user_id, first_name, username)
                VALUES (?, ?, ?)
            """, (
                bale_user_id,
                user_data.get("first_name"),
                user_data.get("username")
            ))

            conn.commit()

            cur.execute("SELECT SCOPE_IDENTITY() AS id")
            return cur.fetchone()[0]