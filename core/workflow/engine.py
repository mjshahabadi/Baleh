from db.database import db_conn


class WorkflowEngine:

    @staticmethod
    def get_workflow(code):

        with db_conn() as conn:
            cur = conn.cursor()

            cur.execute("""
                SELECT id FROM baleh.workflows
                WHERE code=?
            """, (code,))

            row = cur.fetchone()

        return row[0] if row else None


    @staticmethod
    def get_step(workflow_id, step_code):

        with db_conn() as conn:
            cur = conn.cursor()

            cur.execute("""
                SELECT step_code, step_type, message,
                       next_step, field_name
                FROM baleh.workflow_steps
                WHERE workflow_id=? AND step_code=?
            """, (workflow_id, step_code))

            row = cur.fetchone()

        if not row:
            return None

        return {
            "code": row[0],
            "type": row[1],
            "message": row[2],
            "next": row[3],
            "field": row[4]
        }


    @staticmethod
    def get_start_step(workflow_id):

        with db_conn() as conn:
            cur = conn.cursor()

            cur.execute("""
                SELECT step_code
                FROM baleh.workflow_steps
                WHERE workflow_id=? AND is_start=1
            """, (workflow_id,))

            row = cur.fetchone()

        return row[0] if row else None