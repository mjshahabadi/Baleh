from collections import defaultdict


# =========================================================
# INLINE
# =========================================================
from collections import defaultdict

def build_inline_keyboard(buttons):

    keyboard = {}

    for btn in buttons:

        # ==========================================
        # SAFE PARSING (FIX CRASH)
        # ==========================================
        if isinstance(btn, dict):

            title = btn.get("button_text") or btn.get("text")
            icon = btn.get("icon", "")
            action = btn.get("callback_data", "")
            row = btn.get("row_index", 0)
            col = btn.get("col_index", 0)

        elif isinstance(btn, (list, tuple)):

            # old format support
            if len(btn) < 3:
                continue

            title = btn[0]
            icon = btn[1] if len(btn) > 1 else ""
            action = btn[2] if len(btn) > 2 else ""
            row = btn[3] if len(btn) > 3 else 0
            col = btn[4] if len(btn) > 4 else 0

        else:
            continue

        text = f"{icon} {title}" if icon else title

        keyboard.setdefault(row, []).append({
            "text": text,
            "callback_data": action,
            "col": col
        })

    # sort rows
    result = []

    for r in sorted(keyboard.keys()):

        row_buttons = sorted(keyboard[r], key=lambda x: x["col"])

        result.append([
            {
                "text": b["text"],
                "callback_data": b["callback_data"]
            }
            for b in row_buttons
        ])

    return {"inline_keyboard": result}

def build_reply_keyboard(buttons):

    rows = {}

    for btn in buttons:

        title, icon, action, row, col, *_ = btn

        text = f"{icon} {title}" if icon else title

        rows.setdefault(row, []).append(text)

    keyboard = []

    for r in sorted(rows):

        keyboard.append(rows[r])

    return {
        "keyboard": keyboard,
        "resize_keyboard": True,
        "one_time_keyboard": False
    }

# =========================================================
# REPLY
# =========================================================
def build_reply_keyboard(buttons):

    rows = defaultdict(list)

    for btn in buttons:

        text = (
            f'{btn["icon"]} {btn["text"]}'
            if btn["icon"]
            else btn["text"]
        )

        rows[btn["row"]].append({
            "text": text,
            "col": btn["col"]
        })

    keyboard = []

    for row in sorted(rows.keys()):

        row_buttons = sorted(
            rows[row],
            key=lambda x: x["col"]
        )

        keyboard.append([
            b["text"]
            for b in row_buttons
        ])

    return {
        "keyboard": keyboard,
        "resize_keyboard": True
    }


# =========================================================
# MAIN BUILDER
# =========================================================
def build_keyboard(buttons, keyboard_type="inline"):

    keyboard_type = str(keyboard_type).strip().lower()

    if keyboard_type == "inline":
        return build_inline_keyboard(buttons)

    if keyboard_type == "reply":
        return build_reply_keyboard(buttons)

    # fallback
    return build_inline_keyboard(buttons)