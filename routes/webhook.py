from flask import Blueprint, request

from services.bale_api import BaleBot

from core.context.extractor import extract_context

from handlers.message_handler import handle_message

from core.router.callback_router import CallbackRouter

webhook_bp = Blueprint("webhook", __name__)

bot = BaleBot("988312613:vllwDledtWgjpM1YRPpg9hycyY0jGlU4-yM")

callback_router = CallbackRouter(bot)


@webhook_bp.route("/webhook", methods=["POST"])
def webhook():

    update = request.json

    # ==========================
    # BUILD CONTEXT
    # ==========================
    ctx = extract_context(update)

    # ==========================
    # MESSAGE
    # ==========================
    if ctx.type == "message":

        handle_message(ctx, bot)

        return "ok"

    # ==========================
    # CALLBACK
    # ==========================
    if ctx.type == "callback":

        callback_router.handle(ctx)

        return "ok"

    return "ok"