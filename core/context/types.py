from dataclasses import dataclass
from typing import Optional


@dataclass
class Context:
    user_id: int
    chat_id: int
    text: Optional[str]
    callback_data: Optional[str]
    raw: dict