from collections import defaultdict


def build_inline_keyboard(buttons):

    rows = defaultdict(list)

    for btn in buttons:

        text = f"{btn['icon']} {btn['title']}".strip()

        rows[btn["row"]].append({
            "text": text,
            "callback_data": btn["action"],
            "col": btn["col"]
        })

    keyboard = []

    for r in sorted(rows.keys()):
        row_buttons = sorted(rows[r], key=lambda x: x["col"])

        if buttons[0].get("align") == "left":
            row_buttons.reverse()

        keyboard.append([
            {
                "text": b["text"],
                "callback_data": b["callback_data"]
            }
            for b in row_buttons
        ])

    return {"inline_keyboard": keyboard}


def build_reply_keyboard(buttons):

    rows = defaultdict(list)

    for btn in buttons:
        text = f"{btn['icon']} {btn['title']}".strip()
        rows[btn["row"]].append(text)

    return {
        "keyboard": [rows[r] for r in sorted(rows)],
        "resize_keyboard": True,
        "one_time_keyboard": False
    }


def build_keyboard(buttons, keyboard_type: str):

    keyboard_type = (keyboard_type or "inline").strip().lower()

    if keyboard_type == "inline":
        return build_inline_keyboard(buttons)

    if keyboard_type == "reply":
        return build_reply_keyboard(buttons)

    raise ValueError(f"Unknown keyboard type: {keyboard_type}")