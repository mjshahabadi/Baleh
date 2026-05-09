from flask import Blueprint, request, jsonify
from core.security import generate_token, verify_bale_init_data
from services.user_service import UserService
import json

# ✅ تعریف Blueprint (همین خط مشکل تو رو حل می‌کنه)
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/auth/miniapp", methods=["POST"])
def miniapp_auth():
    data = request.json
    init_data = data.get("initData")

    if not init_data:
        return jsonify({"error": "no initData"}), 400

    verified = verify_bale_init_data(init_data)

    if not verified:
        return jsonify({"error": "invalid signature"}), 401

    user_json = verified.get("user", [None])[0]
    user = json.loads(user_json)

    user_id = UserService.get_or_create_user({
        "from": user
    })

    token = generate_token(str(user_id))

    return jsonify({"token": token})