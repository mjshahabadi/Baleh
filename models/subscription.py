class Subscription:
    def __init__(self, user_id, plan_id, start_date, end_date, is_active):
        self.user_id = user_id
        self.plan_id = plan_id
        self.start_date = start_date
        self.end_date = end_date
        self.is_active = is_active