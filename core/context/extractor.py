from core.context.context import Context


def extract_context(update):

    ctx = Context()

    # ==========================================
    # MESSAGE
    # ==========================================
    if "message" in update:

        message = update["message"]

        ctx.update = update
        ctx.message = message

        ctx.chat_id = (
            message.get("chat", {})
                   .get("id")
        )

        ctx.user_id = (
            message.get("from", {})
                   .get("id")
        )

        ctx.text = message.get("text")

        ctx.message_id = message.get("message_id")

        ctx.type = "message"

        return ctx

    # ==========================================
    # CALLBACK
    # ==========================================
    if "callback_query" in update:

        callback = update["callback_query"]

        message = callback.get("message", {})

        ctx.update = update
        ctx.callback = callback
        ctx.message = message

        ctx.chat_id = (
            message.get("chat", {})
                   .get("id")
        )

        ctx.user_id = (
            callback.get("from", {})
                    .get("id")
        )

        ctx.callback_data = callback.get("data")

        ctx.message_id = message.get("message_id")

        ctx.type = "callback"

        return ctx

    return ctx