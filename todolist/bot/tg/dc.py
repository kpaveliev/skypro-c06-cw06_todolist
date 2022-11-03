from dataclasses import dataclass, field
from typing import List, Optional

from marshmallow import EXCLUDE


@dataclass
class MessageFrom:
    """Telegram API: https://core.telegram.org/bots/api#user"""
    id: int
    first_name: str
    last_name: str
    username: str

    class Meta:
        unknown = EXCLUDE


@dataclass
class Chat:
    """Telegram API: https://core.telegram.org/bots/api#chat"""
    id: int
    type: str
    first_name: str
    last_name: str
    username: str
    title: Optional[str] = field(default=None)

    class Meta:
        unknown = EXCLUDE


@dataclass
class Message:
    """Telegram API: https://core.telegram.org/bots/api#message"""
    message_id: int
    from_: MessageFrom = field(metadata=dict(data_key='from'))  # to override usage of keyword "from"
    chat: Chat
    text: str

    class Meta:
        unknown = EXCLUDE


@dataclass
class UpdateObj:
    """Telegram API: https://core.telegram.org/bots/api#getting-updates"""
    update_id: int
    message: Message

    class Meta:
        unknown = EXCLUDE


@dataclass
class GetUpdatesResponse:
    """https://core.telegram.org/bots/api#getupdates"""
    ok: bool
    result: List[UpdateObj]

    class Meta:
        unknown = EXCLUDE


@dataclass
class SendMessageResponse:
    """https://core.telegram.org/bots/api#sendmessage"""
    ok: bool
    result: Message

    class Meta:
        unknown = EXCLUDE
