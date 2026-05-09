from flask import Blueprint, jsonify
from db.database import db_conn

plan_bp = Blueprint("plan", __name__)

@plan_bp.route("/plans", methods=["GET"])
def get_plans():
    with db_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT Id, Name, Price, DurationDays FROM Plans WHERE IsActive = 1")

        plans = []
        for row in cur.fetchall():
            plans.append({
                "id": row.Id,
                "name": row.Name,
                "price": row.Price,
                "duration": row.DurationDays
            })

        return jsonify(plans)