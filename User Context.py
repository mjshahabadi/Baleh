class UserContext:

    def __init__(self, user_id):
        self.user_id = user_id
        self.data = self.load_user()

    def load_user(self):
        return {
            "id": self.user_id,
            "role": "user",
            "has_subscription": True,
            "country": "IR"
        }