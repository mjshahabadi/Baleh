from services.subscription_service import SubscriptionService

def require_subscription(user_id: int):
    return SubscriptionService.has_access(user_id)