from flask import Blueprint, request, jsonify
from services.subscription_service import SubscriptionService
import jwt
from core.security import SECRET_KEY

sub_bp = Blueprint("sub", __name__)

def get_user_from_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return int(payload["user_id"])
    except:
        return None

@sub_bp.route("/subscription/buy", methods=["POST"])
def buy_subscription():
    auth = request.headers.get("Authorization")
    if not auth:
        return jsonify({"error": "unauthorized"}), 401

    token = auth.split(" ")[1]
    user_id = get_user_from_token(token)

    if not user_id:
        return jsonify({"error": "invalid token"}), 401

    plan_id = request.json.get("plan_id")

    ok, result = SubscriptionService.create_subscription(user_id, plan_id)

    if not ok:
        return jsonify({"error": result}), 400

    return jsonify({
        "message": "subscription activated",
        "expire_at": str(result)
    })