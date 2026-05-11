from collections import defaultdict


# =========================================================
# HELPERS
# =========================================================
def _button_value(btn, key, tuple_index=None, default=None):
    if isinstance(btn, dict):
        return btn.get(key, default)

    if isinstance(btn, (list, tuple)) and tuple_index is not None:
        if len(btn) > tuple_index:
            return btn[tuple_index]

    return default


def _button_label(btn):
    title = (
        _button_value(btn, "button_text", 0)
        or _button_value(btn, "text", 0)
        or ""
    )
    icon = _button_value(btn, "icon", 1, "") or ""

    return f"{icon} {title}" if icon else str(title)


def _button_row(btn):
    return int(
        _button_value(btn, "row", default=None)
        if _button_value(btn, "row", default=None) is not None
        else _button_value(btn, "row_index", 3, 0) or 0
    )


def _button_col(btn):
    return int(
        _button_value(btn, "col", default=None)
        if _button_value(btn, "col", default=None) is not None
        else _button_value(btn, "col_index", 4, 0) or 0
    )


def _button_callback(btn):
    return (
        _button_value(btn, "callback_data", 2)
        or _button_value(btn, "action", 2)
        or ""
    )


# =========================================================
# INLINE
# =========================================================
def build_inline_keyboard(buttons):

    rows = defaultdict(list)

    for btn in buttons:
        text = _button_label(btn)
        if not text:
            continue

        rows[_button_row(btn)].append({
            "text": text,
            "callback_data": str(_button_callback(btn)),
            "col": _button_col(btn),
        })

    keyboard = []

    for row in sorted(rows.keys()):
        row_buttons = sorted(rows[row], key=lambda item: item["col"])
        keyboard.append([
            {
                "text": button["text"],
                "callback_data": button["callback_data"],
            }
            for button in row_buttons
        ])

    return {"inline_keyboard": keyboard}


# =========================================================
# REPLY
# =========================================================
def build_reply_keyboard(buttons):

    rows = defaultdict(list)

    for btn in buttons:
        text = _button_label(btn)
        if not text:
            continue

        rows[_button_row(btn)].append({
            "text": text,
            "col": _button_col(btn),
        })

    keyboard = []

    for row in sorted(rows.keys()):
        row_buttons = sorted(rows[row], key=lambda item: item["col"])
        keyboard.append([button["text"] for button in row_buttons])

    return {
        "keyboard": keyboard,
        "resize_keyboard": True,
        "one_time_keyboard": False,
    }


# =========================================================
# MAIN BUILDER
# =========================================================
def build_keyboard(buttons, keyboard_type="inline"):

    keyboard_type = str(keyboard_type or "inline").strip().lower()

    if keyboard_type == "reply":
        return build_reply_keyboard(buttons)

    return build_inline_keyboard(buttons)
