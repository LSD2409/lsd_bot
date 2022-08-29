from sqlalchemy.orm import Session

from app.utils import get_db
from app.core.config import settings

from . import enums, crud, schemas

from chats import crud as chat_crud
from chats import models as chat_models
from chats import schemas as chat_schemas

from datetime import datetime, timezone, timedelta


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
        db = get_db()
        content = None

        if content_type == enums.ContentType.TIMER.name:
            current_time = datetime.now(tz=timezone(timedelta(hours=settings.TZ_OFFSET)))
            time_difference = settings.TIMER - current_time
            hours = time_difference.seconds // 3600
            minutes = abs((hours * 3600 - time_difference.seconds) // 60)
            seconds = 60 - (hours * 3600 + minutes * 60 - time_difference.seconds)
            return f'Осталось {time_difference.days} дней, {hours} часов, {minutes} минут, {seconds} секунд'
        else:
            try:
                content = crud.get_not_consumed_content(
                    db,
                    schemas.NotConsumedContent(
                        content_type=content_type,
                        chat_id=chat_id
                    )
                ).content

            except Exception as e:
                content = 'Закончилось'

        db.close()
        return content