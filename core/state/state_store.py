import json
from db.database import db_conn


class StateStore:

    # ==========================================
    # SET / UPDATE STATE
    # ==========================================
    @staticmethod
    def set_state(user_id: int, workflow_code: str, current_step: str, data: dict = None):

        state_json = json.dumps(data or {}, ensure_ascii=False)

        with db_conn() as conn:
            cur = conn.cursor()

            cur.execute("""

                IF EXISTS (
                    SELECT 1 FROM baleh.user_state WHERE user_id = ?
                )
                BEGIN

                    UPDATE baleh.user_state
                    SET
                        workflow_code = ?,
                        current_step = ?,
                        state_data = ?,
                        updated_at = GETDATE()
                    WHERE user_id = ?

                END
                ELSE
                BEGIN

                    INSERT INTO baleh.user_state
                    (
                        user_id,
                        workflow_code,
                        current_step,
                        state_data,
                        is_completed,
                        created_at,
                        updated_at
                    )
                    VALUES
                    (
                        ?,
                        ?,
                        ?,
                        ?,
                        0,
                        GETDATE(),
                        GETDATE()
                    )

                END

            """, (
                user_id,

                workflow_code,
                current_step,
                state_json,
                user_id,

                user_id,
                workflow_code,
                current_step,
                state_json
            ))

            conn.commit()

    # ==========================================
    # GET STATE
    # ==========================================
    @staticmethod
    def get_state(user_id: int):

        with db_conn() as conn:
            cur = conn.cursor()

            cur.execute("""
                SELECT workflow_code, current_step, state_data
                FROM baleh.user_state
                WHERE user_id = ?
            """, (user_id,))

            row = cur.fetchone()

        if not row:
            return None

        try:
            data = json.loads(row[2] or "{}")
        except:
            data = {}

        return {
            "workflow_code": row[0],
            "current_step": row[1],
            "data": data
        }

    # ==========================================
    # CLEAR STATE
    # ==========================================
    @staticmethod
    def clear_state(user_id: int):

        with db_conn() as conn:
            cur = conn.cursor()

            cur.execute("""
                DELETE FROM baleh.user_state
                WHERE user_id = ?
            """, (user_id,))

            conn.commit()