from sqlalchemy.orm import Session

from . import models, enums

from chats import crud as chat_crud
from chats import models as chat_models
from chats import schemas as chat_schemas


class ContentManager:
    """
    Class for managing content.
    Providing new content for user.
    """

    def __init__(self, chat_id: int, db: Session):
        """Creating new content manager for chat with chat_id if it doesn't exist."""

        chat = chat_crud.get_chat(db, chat_id)
        if not chat:
            chat = chat_crud.create_chat(db, chat_schemas.ChatCreate(chat_id=chat_id))
        self._chat = chat

    @property
    def chat(self) -> chat_models.Chat:
        return self._chat

    def get_content(self, content_type: str, chat_id: int) -> str | None:
        match content_type:
            case enums.ContentType.COMPLIMENT.value:
                pass
            case _:
                return None
