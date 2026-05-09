from services.user_service import UserService
from services.subscription_service import SubscriptionService

from core.access import require_subscription

from services.ui_service import UIService
from ui.keyboard_builder import build_keyboard

from services.state_service import handle_state
from services.workflow_service import handle_workflow


# =========================================================
# GENERIC MENU RENDERER
# =========================================================
def send_menu(bot, chat_id, menu_name, text=None):

    buttons, keyboard_type = UIService.get_menu(menu_name)

    keyboard = build_keyboard(buttons, keyboard_type)

    bot.send_message(
        chat_id,
        text or "📋 منو",
        reply_markup=keyboard
    )


# =========================================================
# MAIN MENU
# =========================================================
def send_main_menu(
    bot,
    chat_id,
    user_id=None
):

    send_menu(
        bot,
        chat_id,
        "main_menu",
        "👋 منوی اصلی:"
    )


# =========================================================
# CHAT ID EXTRACTOR (legacy safe)
# =========================================================
def get_chat_id(update):

    # support both dict and context
    if hasattr(update, "chat_id"):
        return update.chat_id

    return (
        update.get("message", {})
              .get("chat", {})
              .get("id")
    )


# =========================================================
# MAIN MESSAGE HANDLER (FIXED FOR CONTEXT ENGINE)
# =========================================================
def handle_message(ctx, bot):

    # ==========================================
    # 🔥 CONTEXT SAFE ACCESS
    # ==========================================
    try:
        message = ctx.message
    except Exception:
        message = None

    chat_id = getattr(ctx, "chat_id", None)
    user_id = getattr(ctx, "user_id", None)
    text = getattr(ctx, "text", "") or ""

    # fallback safety (if old dict still passes somewhere)
    if message is None and hasattr(ctx, "get"):
        message = ctx.get("message", {})

    if not chat_id and message:
        chat_id = message.get("chat", {}).get("id")

    if not user_id and message:
        user_id = message.get("from", {}).get("id")

    if not chat_id:
        print("NO CHAT ID")
        return

    print("chat_id:", chat_id)
    print("text:", text)

    # ==========================================
    # CREATE USER
    # ==========================================
    if message:
        UserService.get_or_create_user(message)

    # ==========================================
    # WORKFLOW ENGINE
    # ==========================================
    if handle_workflow(bot, message or ctx):
        return

    # ==========================================
    # STATE ENGINE
    # ==========================================
    if handle_state(bot, message or ctx):
        return

    # ==========================================
    # COMMANDS
    # ==========================================
    if text == "/start":

        send_main_menu(
            bot,
            chat_id,
            user_id
        )

        return

    # ==========================================
    # BUY
    # ==========================================
    elif text == "/buy":

        ok, result = SubscriptionService.create_subscription(
            user_id,
            plan_id=1
        )

        if ok:

            bot.send_message(
                chat_id,
                f"اشتراک فعال شد ✅\nتا تاریخ: {result}"
            )

        else:

            bot.send_message(
                chat_id,
                result
            )

        return

    # ==========================================
    # VIP
    # ==========================================
    elif text == "/vip":

        if not require_subscription(user_id):

            bot.send_message(
                chat_id,
                "❌ دسترسی ندارید. ابتدا اشتراک بخرید (/buy)"
            )

            return

        bot.send_message(
            chat_id,
            "🔥 این محتوای ویژه است!"
        )

        return
    # ==========================================
    # REPLY MENU HANDLER (FIX)
    # ==========================================
    reply_menu = UIService.get_menu_by_text(text)

    if reply_menu:

        send_menu(
            bot,
            chat_id,
            reply_menu
        )

        return

    # ==========================================
    # FALLBACK
    # ==========================================
    bot.send_message(
        chat_id,
        "دستور نامعتبر"
    )