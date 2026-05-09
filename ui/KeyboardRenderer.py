class KeyboardRenderer:

    @staticmethod
    def inline(rows):

        keyboard = []

        for r in sorted(rows):

            row = rows[r]

            if row and row[0]["align"] == "left":
                row = list(reversed(row))

            keyboard.append([
                {
                    "text": f"{b['icon']} {b['text']}".strip(),
                    "callback_data": b["action"]
                }
                for b in row
            ])

        return {"inline_keyboard": keyboard}


    @staticmethod
    def reply(rows):

        keyboard = []

        for r in sorted(rows):
            keyboard.append([
                f"{b['icon']} {b['text']}".strip()
                for b in rows[r]
            ])

        return {
            "keyboard": keyboard,
            "resize_keyboard": True
        }