from services.subscription_service import SubscriptionService

def require_subscription(user_id):
    if not SubscriptionService.get_active(user_id):
        return False, "⛔ برای استفاده باید اشتراک داشته باشید"
    return True, None