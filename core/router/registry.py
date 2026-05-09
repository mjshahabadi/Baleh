class RouterRegistry:

    def __init__(self):
        self.routes = {}

    def register(self, key, handler):
        self.routes[key] = handler

    def handle(self, key, bot, callback):

        if key in self.routes:
            return self.routes[key](bot, callback)

        bot.send_message(
            callback["message"]["chat"]["id"],
            "❌ اکشن تعریف نشده"
        )


router = RouterRegistry()