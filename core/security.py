import hashlib
import hmac
import jwt
import datetime
from urllib.parse import parse_qs

from core.config import Config

# 🔐 کلید JWT (حتماً از env بخون بعداً)
SECRET_KEY = Config.BOT_TOKEN  # موقت، بهتره جدا باشه

# =========================
# 🔐 JWT
# =========================

def generate_token(user_id: str):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except:
        return None


# =========================
# 🔐 Bale MiniApp Verify
# =========================

def verify_bale_init_data(init_data: str):
    parsed = parse_qs(init_data)

    received_hash = parsed.pop("hash", [None])[0]
    if not received_hash:
        return None

    # مرتب‌سازی داده‌ها
    data_check_string = "\n".join(
        f"{k}={v[0]}" for k, v in sorted(parsed.items())
    )

    secret_key = hashlib.sha256(Config.BOT_TOKEN.encode()).digest()

    computed_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    ).hexdigest()

    if computed_hash != received_hash:
        return None

    return parsed