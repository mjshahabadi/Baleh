from flask import Blueprint, jsonify
from db.database import db_conn

plan_bp = Blueprint("plan", __name__)


@plan_bp.route("/plans", methods=["GET"])
def get_plans():
    with db_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT Id, title, Price, duration_days
            FROM baleh.Plans
            WHERE ISNULL(IsActive, 1) = 1
            ORDER BY Id
        """)

        plans = []
        for row in cur.fetchall():
            plans.append({
                "id": row[0],
                "name": row[1],
                "price": row[2],
                "duration": row[3]
            })

        return jsonify(plans)
