def start_leave_flow(bot, chat_id, state_mgr):

    state_mgr.set("LEAVE_STEP_1")

    bot.send_message(
        chat_id,
        "📅 تاریخ شروع مرخصی را وارد کنید:"
    )


def handle_leave_flow(bot, chat_id, text, state_mgr):

    if state_mgr.is_state("LEAVE_STEP_1"):

        state_mgr.update(start_date=text)
        state_mgr.set("LEAVE_STEP_2")

        bot.send_message(chat_id, "📅 تاریخ پایان را وارد کنید:")
        return

    if state_mgr.is_state("LEAVE_STEP_2"):

        state_mgr.update(end_date=text)

        data = state_mgr.data

        state_mgr.clear()

        bot.send_message(
            chat_id,
            f"✅ ثبت شد\nاز {data['start_date']} تا {data['end_date']}"
        )