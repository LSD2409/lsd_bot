from pydantic import BaseModel

from datetime import datetime


class ChatBase(BaseModel):
    chat_id: int


class ChatCreate(ChatBase):
    pass


class Chat(ChatBase):
    id: int
    messages: list["ChatMessage"]
    last_message_at: datetime

    class Config:
        orm_mode = True


class ChatMessageBase(BaseModel):

    text: str


class ChatMessageCreate(ChatMessageBase):
    chat_id: int | None = None


class ChatMessage(ChatMessageBase):
    id: int
    chat: Chat
    received_at: datetime

    class Config:
        orm_mode = True
