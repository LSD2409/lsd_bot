from datetime import datetime

from pydantic import BaseModel

from chats import schemas as chats_schemas


class ContentBase(BaseModel):
    content_type: str
    content: str


class ContentCreate(ContentBase):
    pass


class Content(ContentBase):
    id: int
    content_consume: list["ContentConsume"]

    class Config:
        orm_mode = True


class ContentConsumeBase(BaseModel):
    chat_id: int
    content_id: int


class ContentConsumeCreate(ContentConsumeBase):
    pass


class ContentConsume(ContentConsumeBase):
    id: int
    chat: chats_schemas.Chat
    content: "Content"
    watched_at: datetime

    class Config:
        orm_mode = True


class NotConsumedContent(BaseModel):
    content_type: str
    chat_id: int

    class Config:
        orm_mode = True
