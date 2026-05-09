from services.workflow_service import start_workflow


def buy_plan(bot, update):
    chat_id = update["message"]["chat"]["id"]
    bot.send_message(chat_id, "💳 خرید اشتراک")


def profile(bot, update):
    chat_id = update["message"]["chat"]["id"]
    bot.send_message(chat_id, "👤 پروفایل")


def support(bot, update):
    chat_id = update["message"]["chat"]["id"]
    bot.send_message(chat_id, "📞 پشتیبانی")


