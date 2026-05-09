from core.state.state_manager import StateManager
from handlers.flows.leave_flow import handle_leave_flow


def handle_state(bot, message):

    user_id = message["from"]["id"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    state_mgr = StateManager(user_id)

    # اگر در فلو هست
    if state_mgr.state and state_mgr.state.startswith("LEAVE"):
        handle_leave_flow(bot, chat_id, text, state_mgr)
        return True

    return False