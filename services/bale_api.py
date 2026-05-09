import requests
import json

class BaleBot:

    def __init__(self, token):
        self.base_url = f"https://tapi.bale.ai/bot{token}"

    def send_message(self, chat_id, text, reply_markup=None):

        url = f"{self.base_url}/sendMessage"

        payload = {
            "chat_id": chat_id,
            "text": text
        }

        if reply_markup:
            payload["reply_markup"] = json.dumps(reply_markup, ensure_ascii=False)

        headers = {
            "Content-Type": "application/json"
        }
        print("FINAL PAYLOAD:", payload)
        res = requests.post(url, json=payload, headers=headers)

        print("BALE RESPONSE:", res.text)

        return res.json()

    def edit_message(self, chat_id, message_id, text, reply_markup=None):

        url = f"{self.base_url}/editMessageText"

        payload = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text
        }

        if reply_markup:
            payload["reply_markup"] = json.dumps(reply_markup, ensure_ascii=False)

        headers = {
            "Content-Type": "application/json"
        }

        res = requests.post(url, json=payload, headers=headers)
        return res.json()